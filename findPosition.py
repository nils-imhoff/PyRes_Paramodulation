from position import Position
from terms import termIsVar, subterm
from unification import mgu

"""
Find all positions of the term term in this term or its subterms
"""


def find_term(term1, term2):
    positions = []

    if termIsVar(term1):
        return []
    subst = mgu(term1, term2)
    if isinstance(term1, list):

        for i in range(len(term1)):
            positions2 = find_term(subterm(term1, [i]), term2)
            for p in positions2:
                p.add_first(i)
                positions.append(p)
    if subst is not None:
        positions.append(Position(subst))

    return positions
