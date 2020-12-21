import unittest
from lexer import Lexer
import substitutions
from unification import mgu
from literals import Literal, atom2String
from derivations import flatDerivation
import clauses
from terms import termIsVar, subterm
import position

def computeAllParamodulates(clause, clauseset):
    para =  []
    positionLit = position.getPositionLiterals(clause)
    for posLit in range(len(positionLit)):
        for cl in range(len(clauseset)):
            clause2 = clauseset.getClause(cl)
            pos = position.getAllPostions(clause2)
            para = paramodulation(clause,posLit, clause2,pos)
    return para


def paramodulation(clause,posLit, clause2, pos):
    print("test")
