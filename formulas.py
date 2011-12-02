#!/usr/bin/env python2.7
# ----------------------------------
#
# Module formulas.py

"""
A simple implementation of first-order formulas and their associated
meta-information. 

See literals.py for the definition of atoms.

A formula is either a first-order-atom, or build from pre-existing
formulas using the various logical connectives and quantifiers:

Assume F,G are arbitrary formulas and X is an arbitrary variable. Then

(~F)
(F&G)
(F|G)
(F->G)
(F<=>G)
(F<~>G)
(F<-G)
(F~&G)
(F~|G)
(![X]:F)
(?[X]:F)

are formulas.

The set of all formulas for a given signature is denoted as
Formulas(P,F,V).

In the external representation, some parentheses can be omitted. Lists
of either conjunctively or disjunctively connected subformula are
assumed to associate left. (F & G & H) is equivalent to ((F&G)&H)

Formulas are represented on two levels: The actual logical formula is
a recursive data structure. This is wrapped in a container that
associates the formula with its meta-information. The implementation
uses literals as the base case, not atoms. That allows us to reuse
some code for parsing and printing infix equality, but also to
represent a formula in Negation Normal Form without any negations in
the frame of the formula.

Copyright 2011 Stephan Schulz, schulz@eprover.org

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
import substitutions
from literals import Literal, parseLiteral, parseLiteralList,\
     literalList2String, litInLitList, oppositeInLitList


class Formula(object):
    """
    A class representing a naked first-order formula
    formula. Operators are represented as strings, an empty operator
    indicates an atomic formula. child1 and child2 are the subformulas
    (child2 may be empty). In the case of atomic formula, child1 is an
    atom (representing a term). In the case of quantified formulae,
    child1 is a plain string (i.e. the term representing the variable)
    and child2 is the formula quantified over.
    """
        
    def __init__(self, op, child1, child2=None):
        """
        Initialize the formula.
        """
        self.op     = op
        self.child1 = child1
        self.child2 = child2
        
    def __repr__(self):
        """
        Return a string representation of the formula.
        """
        if not self.op:
            res=str(self.child1)
        elif self.op=="~":
            res="(~"+repr(self.child1)+")"
        elif self.op in ["&", "|", "->", "<-", "<=>", "<~>", "~|", "~&"]:
            res = "("+repr(self.child1)+self.op+repr(self.child2)+")"
        else:
            assert self.op in ["!", "?"]
            res = "("+self.op+"["+term2String(self.child1)+\
                  "]:"+repr(self.child2)+")"
        return res   



def parseQuantified(lexer, quantor):
    """
    Parse the "remainder" of a formula starting with the given
    quantor. 
    """
    lexer.CheckTok(Token.IdentUpper)
    var = parseTerm(lexer)
    if lexer.TestTok(Token.Comma):
        lexer.AcceptTok(Token.Comma)
        rest = parseQuantified(lexer, quantor)
    else:
        lexer.AcceptTok(Token.CloseSquare)
        lexer.AcceptTok(Token.Colon)
        rest = parseUnitaryFormula(lexer)
    res = Formula(quantor, var, rest)
    return res
    

def parseUnitaryFormula(lexer):
    """
    Parse a "unitary" formula (following TPTP-3 syntax
    terminology). This can be the first unitary formula of a binary
    formula, of course.
    """
    if lexer.TestTok([Token.Exclamation, Token.Question]):
        quantor = lexer.LookLit()
        lexer.Next()
        lexer.AcceptTok(Token.OpenSquare)
        res = parseQuantified(lexer, quantor)
    elif lexer.TestTok(Token.OpenPar):
        lexer.AcceptTok(Token.OpenPar)
        res = parseFormula(lexer)
        lexer.AcceptTok(Token.ClosePar)
    elif lexer.TestTok(Token.Negation):
        lexer.AcceptTok(Token.Negation)
        subform = parseUnitaryFormula(lexer)
        res = Formula("~", subform, None)
    else:
        lit = parseLiteral(lexer)
        res = Formula("", lit, None)
    return res
    

def parseAssocFormula(lexer, head):
    """
    Parse the rest of the associative formula that starts with head
    and continues ([&|] form *).
    """
    op = lexer.LookLit()
    while lexer.TestLit(op):
        lexer.AcceptLit(op)
        next = parseUnitaryFormula(lexer)
        print next
        head = Formula(op, head, next)
    return head


def parseFormula(lexer):
    """
    Parse a (naked) formula. 
    """
    res = parseUnitaryFormula(lexer)
    if lexer.TestTok([Token.Or, Token.And]):
        res = parseAssocFormula(lexer, res)
    elif lexer.TestTok([Token.Nor, Token.Nand, Token.Equiv,
                        Token.Xor, Token.Implies, Token.BImplies]):
        op = lexer.LookLit()
        rest = parseUnitaryFormula(lexer)
        res = Formula(op, res, rest)
    return res

    

class TestFormulas(unittest.TestCase):
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
        self.nformulas = """![X]:(a(x) | ~a=b)
"""
        self.wformulas = """
"""
       
    def testNakedFormula(self):
        """
        Test that basic parsing works.
        """
        lex = Lexer(self.nformulas)
        f1 = parseFormula(lex)
        print f1
        
        
if __name__ == '__main__':
    unittest.main()