from terms import termIsVar, subterm

"""
Replace term on position position by the term term and substitute everything else
"""


def termReplaceSubstitute(term1, pos, term2):
    new_parameters = []
    if pos.is_final():
        return term2
    if termIsVar(term1):
        return None
    if isinstance(term1, list):
        for i in range(len(term1)):
            if i == pos.get_first():
                t = termReplaceSubstitute(subterm(term1, [i]), pos.pop(), term2)
                if t is None:
                    print("term1")
                new_parameters.append(t)
            else:
                t = pos.get_unifier().apply(subterm(term1, [i]))
                if t is None:
                    print("term1")
                new_parameters.append(t)

    return new_parameters
