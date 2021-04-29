from unittest import TestCase

import clauses
import literals
import paracontrol
import position
import rewriterule
import substitutions
from lexer import Lexer


class TestClause(TestCase):

    def setUp(self):
        """
        Setup function for paramodulation testing
        """
        self.spec = """
cnf(commutativity_of_addition,axiom,
    ( add(A,B) = add(B,A) )).

cnf(associativity_of_addition,axiom,
    ( add(A,add(B,C)) = add(add(A,B),C) )).

cnf(commutativity2,axiom,
    ( subtract(add(A,B),C) = add(subtract(A,C),B) )).

cnf(add_substitution1,axiom,
    ( A != B
    | C != add(A,D)
    | C = add(B,D) )).


cnf(prove_equation,negated_conjecture,
    ( add(add(a,b),c) != add(a,add(b,c)) )).
    """
        lex = Lexer(self.spec)
        self.c1 = clauses.parseClause(lex)
        self.c2 = clauses.parseClause(lex)
        self.c3 = clauses.parseClause(lex)
        self.c4 = clauses.parseClause(lex)
        self.c5 = clauses.parseClause(lex)

    def test_find_should_succeed_term_is_found(self):
        pos = self.c1.find(['add', 'A', 'B'])
        pos2 = self.c2.find(['add', 'A', 'B'])
        subst1 = substitutions.Substitution()
        subst2 = substitutions.Substitution([('B', 'A')])
        subst3 = substitutions.Substitution([('B', 'A'), ('C', 'A')])
        expectedPos1 = position.Position(subst1, [0, 1])
        expectedPos2 = position.Position(subst2, [0, 2])
        expectedPos3 = position.Position(subst3, [0, 1, 2])
        expectedPos4 = position.Position(subst1, [0, 2, 1])

        self.assertEqual(2, len(pos))
        self.assertEqual(expectedPos1, pos[0])
        self.assertEqual(expectedPos2, pos[1])

        self.assertEqual(2, len(pos2))
        self.assertEqual(expectedPos3, pos2[0])
        self.assertEqual(expectedPos4, pos2[1])

    def test_createRewriteRule_should_succeed_if_rule_is_created(self):
        rewrite_rules1 = paracontrol.createRewriteRule(self.c1)
        rewrite_rules2 = paracontrol.createRewriteRule(self.c4)

        expectedLiteral1 = literals.Literal(['=', 'A', 'B'], True)
        expectedLiteral2 = literals.Literal(['=', 'C', ['add', 'A', 'D']], True)
        expectedLiterals = [expectedLiteral1, expectedLiteral2]
        expectedRewriteRule1 = rewriterule.rewriteRule(['add', 'A', 'B'], ['add', 'B', 'A'], [], self.c1)
        expectedRewriteRule2 = rewriterule.rewriteRule(['add', 'B', 'A'], ['add', 'A', 'B'], [], self.c1)
        expectedRewriteRule3 = rewriterule.rewriteRule('C', ['add', 'B', 'D'], expectedLiterals, self.c4)
        expectedRewriteRule4 = rewriterule.rewriteRule(['add', 'B', 'D'], 'C', expectedLiterals, self.c4)

        self.assertEqual(2, len(rewrite_rules1))
        self.assertEqual(expectedRewriteRule1, rewrite_rules1[0])
        self.assertEqual(expectedRewriteRule2, rewrite_rules1[1])

        self.assertEqual(2, len(rewrite_rules2))
        self.assertEqual(expectedRewriteRule3, rewrite_rules2[0])
        self.assertEqual(expectedRewriteRule4, rewrite_rules2[1])

    def test_createRewriteRule_should_succeed_if_no_rule_created(self):
        rewrite_rules = paracontrol.createRewriteRule(self.c5)
        self.assertEqual(0, len(rewrite_rules))

    def test_replaceSubstitute_should_succeed_if_new_clause_is_correct(self):
        subst = substitutions.Substitution()
        pos = position.Position(subst, [0, 1, 1, ])
        clause = self.c3.replaceSubstitute(pos, ['add', 'B', 'A'])
        expectedLiteral = literals.Literal(['=', ['subtract', ['add', 'B', 'A'], 'C'], ['add', ['subtract', 'A', 'C'], 'B']])
        expectedClause = clauses.Clause([expectedLiteral])
        self.assertEqual(expectedClause.compare(clause), True)

    def test_apply_should_succeed_if_new_clauses_are_correct(self):
        to = ['add', 'B', 'A']
        frm = ['add', 'A', 'B']
        expectedLiteral = literals.Literal(
            ['=', ['subtract', ['add', 'B', 'A'], 'C'], ['add', ['subtract', 'A', 'C'], 'B']])
        expectedClause = clauses.Clause([expectedLiteral])
        rewrite_rule = rewriterule.rewriteRule(frm, to, [], self.c1)
        res = rewrite_rule.apply(self.c3)
        print(res[0].evaluation)
        print(expectedClause.evaluation)
        self.assertTrue(expectedClause.compare(res[0]))

