import clauses
from terms import termIsVar, subterm
import literals


def getAllPostions(clause):
    positionLit = []
    positionSubterm = []
    position = {'lit': positionLit, 'subterms': positionSubterm}
    for lit in range(len(clause)):
        l = clause.getLiteral(lit)
        positionLit.append([lit])
        ap = getPositionSubterm(l)
        positionSubterm.append(ap)
    position['lit'].extend(positionLit)
    position['subterms'].extend(positionSubterm)
    return position


def getPositionSubterm(lit):
    positionSubterm = []
    for a in range(len(lit.atom)):
        erg = getSubterms(a,lit.atom)
        if erg != None:
            positionSubterm.append(erg)
        else:
            print("HIER")
    return positionSubterm

def getSubterms(a,l):
    positionSubterm = []
    t = subterm(l, [a])
    if not termIsVar(t) and t != None:
       print("A A A" + str(a))
       positionSubterm.append([a])
    elif t == None or termIsVar(t):
        return None
    if isinstance(t, list):
        for b in range(len(t)):
         erg = getSubterms(b,t)
         if erg != None:
            positionSubterm.append(erg)
    return positionSubterm


def getPositionLiterals(clause):
    positionLit = []
    for lit in range(len(clause)):
        l1 = clause.getLiteral(lit)
        if l1.atom[0] == 'eq' and l1.isPositive():
            positionLit.append(lit)
    return positionLit
