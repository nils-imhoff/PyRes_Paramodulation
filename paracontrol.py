from rewriterule import rewriteRule


def computeAllParamodulates(clause, clauseset):
    res = []
    rewrite_rules = createRewriteRule(clause)
    if rewrite_rules:
        clause = clause.freshVarCopy()
        res.extend(paramodulation(clause, rewrite_rules))
        for i in range(len(clauseset)):
            res.extend(paramodulation(clauseset.clauses[i], rewrite_rules))

    return res


def createRewriteRule(given_clause):
    new_rewrite_rules = []
    for l in range(len(given_clause)):
        lit = given_clause.getLiteral(l)
        if lit.atom[0] == '=' and not lit.isNegative():
            left = lit.atom[1]
            right = lit.atom[2]

            new_literals = []

            for ll in range(len(given_clause)):
                lit2 = given_clause.getLiteral(ll)
                if lit2 != lit:
                    new_literals.append(lit2)

            left_rule = rewriteRule(left, right, new_literals, given_clause)
            right_rule = rewriteRule(right, left, new_literals, given_clause)

            new_rewrite_rules.append(left_rule)
            new_rewrite_rules.append(right_rule)

    return new_rewrite_rules


def paramodulation(given_clause, rewrite_rules):
    res = []
    for r in rewrite_rules:
        res.extend(r.apply(given_clause))

    return res
