from clauses import Clause
from derivations import flatDerivation
from unification import mgu

"""
E-resolution inference step
"""


def eresolution(clause) -> list:
    res = []
    for l in range(len(clause)):
        lit = clause.getLiteral(l)
        if lit.atom[0] == '=' and lit.isNegative():
            left = lit.atom[1]
            right = lit.atom[2]

            unifier = mgu(left, right)
            if unifier is not None:
                others = []

                for ll in range(len(clause)):
                    lit2 = clause.getLiteral(ll)
                    if ll != l:
                        if unifier is None:
                            others.append(lit2)
                        else:
                            others.append(lit2.instantiate(unifier))

                new_clause = Clause(others)

                new_clause.setDerivation(flatDerivation("eresolution", [clause, clause]))

                res.append(new_clause)
    return res
