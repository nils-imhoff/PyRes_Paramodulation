#!/usr/bin/env python2.7
# ----------------------------------
#
# Module literal.py

"""
A simple implementation of first-order atoms and literals.

We assume a set of function symbols F (with associated arities) and
variables symbols as defined in terms.py. We now also assume a set P
of predicate symbols, and extend the arity function to
ar:F \cup P ->N

The set of all first-order atoms over P, F, V, Atom(P,F,V) is defined
as follows:
- If t1, ... t_n are in Term(F,V) and p|n is in P, then p(t1,..., tn)
  is in Atom(P,F,V)
- Atom(P,F,V) is the smallest set with this property.


Assume F={f|2, g|1, a|0, b|0}, V={X, Y, ...} and P={p|1, q|2}. Then
the following are atoms:

p(a)
q(X, g(g(a)))
p(f(b, Y))

Because of the special role of equality for theorem proving, we
usually assume "="|2 and "!="|2 are in P. In the concrete syntax,
these symbols are written as infix symbols, i.e. we write a=b, not
"=(a, b)".

A literal is a signed atom. A positive literal is syntactically
identical to its atom. A negative literal consists of the negation
sign, ~, followed by an atom.

We establish the convention that t1!=t2 is equivalent to ~t1=t2  and
~t1!=t2 is equivalent to t1=t2, and only use the respective later
forms internally. In other words, the symbol != only occurs during
parsing and printing. 


Copyright 2010-2011 Stephan Schulz, schulz@eprover.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program ; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307 USA 

The original copyright holder can be contacted as

Stephan Schulz
Hirschstrasse 35
76133 Karlsruhe
Germany
Email: schulz@eprover.org
"""

import unittest
from lexer import Token,Lexer
from terms import *




def parseAtom(lexer):
    """
    Parse an atom. An atom is either a conventional atom, in which
    case it's syntactically identical to a term, or it is an
    equational literal, of the form 't1=t2' or 't1!=t2', where t1 and
    t2 are terms.

    In either case, we represent the atom as a first-order
    term. Equational literals are represented at terms with faux
    function symbols "=" and "!=". 
    """
    atom = parseTerm(lexer)
    if lexer.TestTok([Token.EqualSign, Token.NotEqualSign]):
        # The literal is equational.
        # We get the actual operator, '=' or '!=', followed by the
        # other side of the (in)equation
        op  = lexer.Next().literal
        lhs = atom
        rhs = parseTerm(lexer)
        atom = list([op, lhs, rhs])        

    return atom
    



class Literal(object):
    """
    A class representing a literal. A literal is a signed atom. We
    already allow for equational atoms with infix "=" or "!="
    operators, and normalize them on creation.
    """
    def __init__(self, atom, negative=False):
        """
        Initialize a literal. Normalize literals with negative
        equational atoms in the process.
        """

        if termFunc(atom) == "!=":
            self.negative = not negative
            self.atom = list(["="])
            self.atom.extend(termArgs(atom))
        else:
            self.negative = negative
            self.atom = atom
        
    def __repr__(self):
        """
        Return a string representation of the literal.
        """
        if self.isEquational():
            op = "="
            if self.isNegative():
                op = "!="
                
            result = term2String(termArgs(self.atom)[0])+\
                     op+\
                     term2String(termArgs(self.atom)[1])
        else:
            if self.isNegative():
                result = "~"+term2String(self.atom)
            else:
                result = term2String(self.atom)
        return result

    def isEquational(self):
        """
        Returm true if the literal is equational.
        """
        return termFunc(self.atom)=="="

    def isNegative(self):
        """
        Return true if the literal is negative.
        """
        return self.negative
    
    def isPositive(self):
        """
        Return true if the literal is positive.
        """
        return not self.negative

    def isEqual(self, other):
        """
        Return true if the literal is structurally identical to
        other.
        """
        return self.isNegative()==other.isNegative() and \
               termEqual(self.atom, other.atom)

    def collectVars(self, res=None):
        """
        Insert all variables in self into the set res and return
        it. If res is not given, create it.
        """
        res = termCollectVars(self.atom, res)
        return res

    def instantiate(self, subst):
        """
        Return a copy of self, instantiated with the given
        subtitution.
        """
        return Literal(subst(self.atom), self.negative)

def parseLiteral(lexer):
    """
    Parse a literal. A literal is an optional negation sign '~',
    followed by an atom.
    """
    negative = False
    if lexer.TestTok(Token.Negation):
        negative = True
        lexer.Next()
    atom = parseAtom(lexer)

    return Literal(atom, negative)
    

def parseLiteralList(lexer):
    """
    Parse a list of literals separated by "|" (logical or). As per
    TPTP 3 syntax, the single word "$false" is interpreted as the
    false literal, and ignored.
    """
    res = []
    if lexer.LookLit()=="$false":
        lexer.Next()
    else:
        lit = parseLiteral(lexer)
        res.append(lit)
    
    while lexer.TestTok(Token.Or):
        lexer.Next()
        
        if lexer.LookLit()=="$false":
            lexer.Next()
        else:
            lit = parseLiteral(lexer)
            res.append(lit)

    return res


def literalList2String(list):
    """
    Convert a literal list to a textual representation that can be
    parsed back.
    """
    if not list:
        return "$false"
    return "|".join(map(repr, list))
    


class TestLiterals(unittest.TestCase):
    """
    Unit test class for clauses. Test clause and literal
    functionality.
    """
    def setUp(self):
        """
        Setup function for clause/literal unit tests. Initialize
        variables needed throughout the tests.
        """
        print
        self.input1="p(X)  ~q(f(X,a), b)  ~a=b  a!=b  ~a!=f(X,b)"
        self.input2="p(X)|~q(f(X,a), b)|~a=b|a!=b|~a!=f(X,b)"
        self.input3="$false"
        self.input4="$false|~q(f(X,a), b)|$false"
        

    def testLiterals(self):
        """
        Test that basic literal parsing and literal functions work
        correctly.
        """
        lexer = Lexer(self.input1)
        a1 = parseLiteral(lexer)
        a2 = parseLiteral(lexer)
        a3 = parseLiteral(lexer)
        a4 = parseLiteral(lexer)
        a5 = parseLiteral(lexer)

        vars = set()
        print a1
        self.assert_(a1.isPositive())
        self.assert_(not a1.isEquational())
        a1.collectVars(vars)
        self.assertEqual(len(vars), 1)
        
        print a2
        self.assert_(a2.isNegative())
        self.assert_(not a2.isEquational())
        a2.collectVars(vars)
        self.assertEqual(len(vars), 1)

        print a3
        self.assert_(a3.isNegative())
        self.assert_(a3.isEquational())
        self.assert_(a3.isEqual(a4))
        a3.collectVars(vars)
        self.assertEqual(len(vars), 1)
        
        print a4
        self.assert_(a4.isNegative())
        self.assert_(a4.isEquational())
        self.assert_(a4.isEqual(a3))
        a4.collectVars(vars)
        self.assertEqual(len(vars), 1)
        
        print a5
        self.assert_(not a5.isNegative())
        self.assert_(a5.isEquational())
        a5.collectVars(vars)
        self.assertEqual(len(vars), 1)
        
    def testLitList(self):
        """
        Test literal list parsing and printing.
        """
        lexer = Lexer(self.input2)
        l2 = parseLiteralList(lexer)
        print literalList2String(l2)
        self.assertEqual(len(l2),5) 

        lexer = Lexer(self.input3)
        l3 = parseLiteralList(lexer)
        print literalList2String(l3)
        self.assertEqual(len(l3),0) 

        lexer = Lexer(self.input4)
        l4 = parseLiteralList(lexer)
        print literalList2String(l4)
        self.assertEqual(len(l4),1) 

        

if __name__ == '__main__':
    unittest.main()
