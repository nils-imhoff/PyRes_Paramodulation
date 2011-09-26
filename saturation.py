#!/usr/bin/env python2.7
# ----------------------------------
#
# Module saturation.py

"""
Implementation of the given-clause algorithm for saturation of clause
sets under the rules of the resolution calculus.

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
from idents import Ident
from lexer import Token,Lexer
from clausesets import ClauseSet, HeuristicClauseSet
import heuristics
from rescontrol import computeAllResolvents, computeAllFactors



class SearchParams(object):
    """
    A simple container for different parameter settings for the proof
    search.    
    """
    def __init__(self,
                 heuristics = heuristics.PickGiven5,
                 delete_tautologies   = False,
                 forward_subsumption  = False,
                 backward_subsumption = False):
                 
                 
        """
        Initialize heuristic parameters.
        """
        self.heuristics           = heuristics
        self.delete_tautologies   = delete_tautologies
        self.forward_subsumption  = forward_subsumption
        self.backward_subsumption = backward_subsumption
                 
        


class ProofState(object):
    """
    Top-level data structure for the prover: Processed and uprocessed
    clause sets, and statistical data.
    """
    def __init__(self, params, clauses):
        """
        Initialize the proof state with a set of clauses.
        """
        self.params = params
        self.unprocessed = HeuristicClauseSet(params.heuristics)
                                     
        self.processed   = ClauseSet()
        for c in clauses.clauses:
            self.unprocessed.addClause(c)
        self.initial_clause_count = len(self.unprocessed)
        self.proc_clause_count    = 0
        self.factor_count         = 0
        self.resolvent_count      = 0
        self.tautologies_deleted  = 0
        
    def processClause(self):
        """
        Pick a clause from unprocessed and process it. If the empty
        clause is found, return it. Otherwise return None.
        """
        given_clause = self.unprocessed.extractBest()
        given_clause = given_clause.freshVarCopy()
        print "#", given_clause
        if given_clause.isEmpty():
            # We have found an explicit contradiction
            return given_clause
        if self.params.delete_tautologies and \
           given_clause.isTautology():
            self.tautologies_deleted = self.tautologies_deleted+1
            return None
            
        new = []
        factors    = computeAllFactors(given_clause)
        new.extend(factors)
        resolvents = computeAllResolvents(given_clause, self.processed)
        new.extend(resolvents)
        self.proc_clause_count = self.proc_clause_count+1
        self.factor_count = self.factor_count+len(factors)
        self.resolvent_count = self.resolvent_count+len(resolvents)
        self.processed.addClause(given_clause)

        for c in new:
            self.unprocessed.addClause(c)
        return None

    def saturate(self):
        """
        Main proof procedure. If the clause set is found
        unsatisfiable, return the empty clause as a witness. Otherwise
        return None.
        """
        while self.unprocessed:
            res = self.processClause()
            if res != None:
                return res
        else:
            return None

    def statisticsStr(self):
        """
        Return the proof state statistics in string form ready for
        output.
        """
        return """
# Initial clauses    : %d
# Processed clauses  : %d
# Factors computed   : %d
# Resolvents computed: %d
# Tautologies deleted: %d""" \
    %(self.initial_clause_count,
      self.proc_clause_count,
      self.factor_count,
      self.resolvent_count,
      self.tautologies_deleted)
        

class TestProver(unittest.TestCase):
    """
    Unit test class for simple resolution inference control.
    """
    def setUp(self):
        """
        Setup function for clause/literal unit tests. Initialize
        variables needed throughout the tests.
        """
        print
        self.params = SearchParams()
        self.params.delete_tautologies = True
        self.spec1 = """
 cnf(axiom, a_is_true, a).
 cnf(negated_conjecture, is_a_true, ~a)."""

        self.spec2 = """
%------------------------------------------------------------------------------
% File     : PUZ001-1 : TPTP v4.1.0. Released v1.0.0.
% Domain   : Puzzles
% Problem  : Dreadbury Mansion
% Version  : Especial.
%            Theorem formulation : Made unsatisfiable.
% English  : Someone who lives in Dreadbury Mansion killed Aunt Agatha.
%            Agatha, the butler, and Charles live in Dreadbury Mansion,
%            and are the only people who live therein. A killer always
%            hates his victim, and is never richer than his victim.
%            Charles hates no one that Aunt Agatha hates. Agatha hates
%            everyone except the butler. The butler hates everyone not
%            richer than Aunt Agatha. The butler hates everyone Aunt
%            Agatha hates. No one hates everyone. Agatha is not the
%            butler. Therefore : Agatha killed herself.

% Refs     : [Pel86] Pelletier (1986), Seventy-five Problems for Testing Au
%          : [MB88]  Manthey & Bry (1988), SATCHMO: A Theorem Prover Implem
% Source   : [TPTP]
% Names    :

% Status   : Unsatisfiable
% Rating   : 0.00 v2.0.0
% Syntax   : Number of clauses     :   12 (   2 non-Horn;   5 unit;  12 RR)
%            Number of atoms       :   21 (   0 equality)
%            Maximal clause size   :    3 (   2 average)
%            Number of predicates  :    4 (   0 propositional; 1-2 arity)
%            Number of functors    :    3 (   3 constant; 0-0 arity)
%            Number of variables   :    8 (   0 singleton)
%            Maximal term depth    :    1 (   1 average)
% SPC      : CNF_UNS_EPR

% Comments : Modified from the [MB88] version to be unsatisfiable, by Geoff
%            Sutcliffe.
%          : Also known as "Who killed Aunt Agatha"
%------------------------------------------------------------------------------
cnf(agatha,hypothesis,
    ( lives(agatha) )).

cnf(butler,hypothesis,
    ( lives(butler) )).

cnf(charles,hypothesis,
    ( lives(charles) )).

cnf(poorer_killer,hypothesis,
    ( ~ killed(X,Y)
    | ~ richer(X,Y) )).

cnf(different_hates,hypothesis,
    ( ~ hates(agatha,X)
    | ~ hates(charles,X) )).

cnf(no_one_hates_everyone,hypothesis,
    ( ~ hates(X,agatha)
    | ~ hates(X,butler)
    | ~ hates(X,charles) )).

cnf(agatha_hates_agatha,hypothesis,
    ( hates(agatha,agatha) )).

cnf(killer_hates_victim,hypothesis,
    ( ~ killed(X,Y)
    | hates(X,Y) )).

cnf(same_hates,hypothesis,
    ( ~ hates(agatha,X)
    | hates(butler,X) )).

cnf(agatha_hates_charles,hypothesis,
    ( hates(agatha,charles) )).

cnf(butler_hates_poor,hypothesis,
    ( ~ lives(X)
    | richer(X,agatha)
    | hates(butler,X) )).

%----Literal dropped from here to make it unsatisfiable
cnf(prove_neither_charles_nor_butler_did_it,negated_conjecture,
    ( killed(butler,agatha)
    | killed(charles,agatha) )).

%------------------------------------------------------------------------------
"""

        self.spec3 = """
cnf(p_or_q, axiom, p(X)|q(a)).
cnf(taut, axiom, p(X)|~p(X)).
cnf(not_p, axiom, ~p(a)).
"""

    def evalSatResult(self, spec, provable):
        """
        Evaluate the result of a saturation compared to the expected
        result.
        """

        lex = Lexer(spec)
        problem = ClauseSet()
        problem.parse(lex)

        prover = ProofState(self.params, problem)
        res = prover.saturate()

        if provable:
            self.assertNotEqual(res, None)
            if res == None: # pragma: nocover
                print "# Bug: Should have found a proof!"
            else:
                print "# Proof found"
        else:
            self.assertEqual(res, None)
            if res != None: # pragma: nocover
                print "# Bug: Should not have  found a proof!"
            else:
                print "# No proof found"
                
        print prover.statisticsStr()
        
    def testSaturation(self):
        """
        Test that saturation works.
        """
        self.evalSatResult(self.spec1, True)
        self.evalSatResult(self.spec2, True)
        self.evalSatResult(self.spec3, False)


    def testParamSet(self):
        """
        Test that parameter setting code works.        
        """
        pm = SearchParams()
        self.assertEqual(pm.heuristics, heuristics.PickGiven5)
        self.assertEqual(pm.delete_tautologies,   False)
        self.assertEqual(pm.forward_subsumption,  False)
        self.assertEqual(pm.backward_subsumption, False)

if __name__ == '__main__':
    unittest.main()