from unittest import TestCase

import clauses
import paracontrol
from lexer import Lexer


class TestClause(TestCase):

    def setUp(self):
        """
        Setup function for resolution testing
        """
        print()
        self.spec = """
cnf(commutativity_of_addition,axiom,
    ( add(A,B) = add(B,A) )).

cnf(associativity_of_addition,axiom,
    ( add(A,add(B,C)) = add(add(A,B),C) )).

cnf(addition_inverts_subtraction1,axiom,
    ( subtract(add(A,B),B) = A )).

cnf(addition_inverts_subtraction2,axiom,
    ( A = subtract(add(A,B),B)  )).

cnf(commutativity1,axiom,
    ( add(subtract(A,B),C) = subtract(add(A,C),B) )).

cnf(commutativity2,axiom,
    ( subtract(add(A,B),C) = add(subtract(A,C),B) )).

cnf(add_substitution1,axiom,
    ( A != B
    | C != add(A,D)
    | C = add(B,D) )).

cnf(add_substitution2,axiom,
    ( A != B
    | C != add(D,A)
    | C != add(D,B) )).

cnf(prove_equation,negated_conjecture,
    ( add(add(a,b),c) != add(a,add(b,c)) )).
    """
        lex = Lexer(self.spec)
        self.c1 = clauses.parseClause(lex)
        self.c2 = clauses.parseClause(lex)
        self.c3 = clauses.parseClause(lex)
        self.c4 = clauses.parseClause(lex)
        self.c5 = clauses.parseClause(lex)
        self.c6 = clauses.parseClause(lex)
        self.c7 = clauses.parseClause(lex)
        self.c8 = clauses.parseClause(lex)
        self.c9 = clauses.parseClause(lex)

    def test_find_should_succeed_term_is_found(self):
        pos = self.c1.find(['add', 'A', 'B'])
        pos2 = self.c2.find(['add', 'A', 'B'])

        self.assertEqual(2, len(pos))
        self.assertEqual([0, 1], pos[0].l)
        self.assertEqual({}, pos[0].get_unifier().subst)
        self.assertEqual([0, 2], pos[1].l)
        self.assertEqual({'B': 'A'}, pos[1].get_unifier().subst)

        self.assertEqual(2, len(pos2))
        self.assertEqual([0, 1, 2], pos2[0].l)
        self.assertEqual({'B': 'A', 'C': 'A'}, pos2[0].get_unifier().subst)
        self.assertEqual([0, 2, 1], pos2[1].l)
        self.assertEqual({}, pos2[1].get_unifier().subst)

    def test_createRewriteRule_should_succeed_if_rule_is_created(self):
        rewrite_rules1 = paracontrol.createRewriteRule(self.c1)
        rewrite_rules2 = paracontrol.createRewriteRule(self.c7)
        self.assertEqual(2, len(rewrite_rules1))
        self.assertEqual(['add', 'A', 'B'], rewrite_rules1[0].get_from())
        self.assertEqual(['add', 'B', 'A'], rewrite_rules1[0].get_to())
        self.assertEqual(['add', 'B', 'A'], rewrite_rules1[1].get_from())
        self.assertEqual(['add', 'A', 'B'], rewrite_rules1[1].get_to())
        self.assertEqual([], rewrite_rules1[0].get_literals())
        self.assertEqual(self.c1, rewrite_rules1[0].clause)

        self.assertEqual(2, len(rewrite_rules2))
        self.assertEqual('C', rewrite_rules2[0].get_from())
        self.assertEqual(['add', 'B', 'D'], rewrite_rules2[0].get_to())
        self.assertEqual(['add', 'B', 'D'], rewrite_rules2[1].get_from())
        self.assertEqual('C', rewrite_rules2[1].get_to())
        self.assertEqual(2, len(rewrite_rules2[0].get_literals()))
        self.assertEqual(['=', 'A', 'B'], rewrite_rules2[0].get_literals()[0].atom)
        self.assertEqual(['=', 'C', ['add', 'A', 'D']], rewrite_rules2[0].get_literals()[1].atom)
        self.assertEqual(self.c7, rewrite_rules2[0].clause)

    def test_createRewriteRule_should_succeed_if_no_rule_created(self):
        rewrite_rules = paracontrol.createRewriteRule(self.c9)
        self.assertEqual(0, len(rewrite_rules))
