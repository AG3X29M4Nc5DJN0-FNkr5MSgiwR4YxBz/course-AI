from utils import *
from logic import *

kb = PropKB()

kb.tell(~P11)
kb.tell(B11 | '<=>' | ((P12 | P21)))
kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))

kb.tell(B11)
kb.tell(~B21)
kb.tell(~P21)

print(kb.clauses)

print(pl_resolution(kb,P21))

#Test Dpll

s = []
s.append(Symbol(P21))
s.append(Symbol(P12))
s.append(Symbol(P11))
s.append(Symbol(P22))
s.append(Symbol(P31))
s.append(Symbol(B11))
s.append(Symbol(B21))
#I wanna know if P12
clauseList = kb.clauses
clauseList.append(expr("P12"))
a = dpll(clauseList,s,{})
print(a)
