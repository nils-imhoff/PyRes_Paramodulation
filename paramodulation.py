import unittest
from lexer import Lexer
import substitutions
from unification import mgu
from literals import Literal, atom2String
from derivations import flatDerivation
import clauses


def computeAllParamodulates(clause, clauseset):
    para = []
    for cl2 in range(len(clauseset)):
        para = (paramodulation(clause, clauseset.getClause(cl2), para))
    return para


def paramodulation(clause1, clause2, para):
    for lit1 in range(len(clause1)):
        l1 = clause1.getLiteral(lit1)
        if(l1.atom[0] == 'eq' and l1.isPositive()):
            lTerm = l1.atom[1]
            rTerm = l1.atom[2]
            otherLit = []
            for lit in range(len(clause1)):
                l = clause1.getLiteral(lit)
                if(l != l1):
                    otherLit.append(l)
            print('otherLit', otherLit)
            for lit2 in range(len(clause2)):
                l2 = clause2.getLiteral(lit2)
                sigmaL = mgu(lTerm, l2.atom)
                print('lTerm', lTerm)
                if sigmaL == None:
                    continue
                litsL1 = [l.instantiate(sigmaL)
                          for l in clause1.literals if l != l1]
                litsL2 = [l.instantiate(sigmaL)
                          for l in clause2.literals if l != l2]
                litsL1.extend(litsL2)
                sigmaR = mgu(rTerm, l2.atom)
                print('rTerm', rTerm)
                if sigmaR == None:
                    continue
                litsR1 = [l.instantiate(sigmaL)
                          for l in clause1.literals if l != l1]
                litsR2 = [l.instantiate(sigmaL)
                          for l in clause2.literals if l != l2]
                litsR1.extend(litsR2) 
                for i in (litsL1):
                    print("war hier")
                    for n in range(len(i.atom)):
                        if i.atom[n] == lTerm:
                            i.atom[n] = rTerm
                para.append(clauses.Clause(litsL1))
                for i in (litsR1):
                    print("war hier")
                    for n in range(len(i.atom)):
                        if i.atom[n] == rTerm:
                            i.atom[n] = lTerm
                para.append(clauses.Clause(litsR1))
                print(para)
    return para
