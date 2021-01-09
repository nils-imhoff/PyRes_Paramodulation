#
# Representation of a paramodulation rewriting rule
# This class contains data for a single rewrite rule, so the equalities dont have to be looked up over and over again.
#
class rewriteRule(object):
    def __init__(self, frm, to, literals, given_clause):
        self.frm = frm
        self.to = to
        self.literals = literals
        self.clause = given_clause

    def get_from(self):
        return self.frm

    def get_to(self):
        return self.to

    def get_literals(self):
        return self.literals

    def apply(self, clause):
        res = []
        positions = clause.find(self.frm)
        if positions is not None:
            for pos in positions:
                new_clause = clause.replace_substitute(pos, self.to.instantiate(pos.get_unifier()))
                if new_clause is not None:
                    for l in self.literals:
                        l = l.instantiate(pos.get_unifier())
                        if l is None:
                            print("rewrite")
                        new_clause.addLiteral(l)
                    res.append(new_clause)
        return res