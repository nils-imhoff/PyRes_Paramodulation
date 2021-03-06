# Class for storing term position


class Position(object):

    def __init__(self, subst, l = None):
        if l is None:
            l = []
        self.l = l
        self.subst = subst

    @classmethod
    def create_new(cls, subst, l):
        return cls(subst=subst, l=l[1:])

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.l == other.l and self.subst.__eq__(other.subst)

    def add_first(self, i):
        self.l.insert(0, i)

    def get_first(self):
        return self.l[0]

    def is_final(self):
        return len(self.l) == 0

    def get_unifier(self):
        return self.subst

    def pop(self):
        return self.create_new(self.subst, self.l)
