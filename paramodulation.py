import unittest
from lexer import Lexer
import substitutions
from unification import mgu
from literals import Literal
from derivations import flatDerivation
import clauses


def computeAllParamodulates(clause, clauseset):
    para = []
    for cl2 in clauseset:
        para = (paramodulation(clause, cl2, para))
    return para


def paramodulation(clause1, clause2, para):
    for l1 in clause1.literals:
        if(l1.atom[0] == '=' and not l1.negative()):
            lTerm = l1.atom[1]
            rTerm = l1.atom[2]
            otherLit = []
            for l in clause1.literals:
                if(l != l1):
                    otherLit.append(l)
            for l2 in clause2.literals:
                sigmaL = [mgu(lTerm, l2.atom)]
                if sigmaL == None:
                    continue
                sigmaR = [mgu(rTerm, l2.atom)]
                if sigmaR == None:
                    continue
                for n, i in enumerate(sigmaL):
                    if i == lTerm:
                        sigmaL[n] = rTerm
                sigmaL.extend(otherLit)
                para.append(clauses.Clause(sigmaL))
                for n, i in enumerate(sigmaR):
                    if i == rTerm:
                        sigmaR = lTerm
                sigmaR.extend(otherLit)
                para.append(clauses.Clause(sigmaR))
    return para
