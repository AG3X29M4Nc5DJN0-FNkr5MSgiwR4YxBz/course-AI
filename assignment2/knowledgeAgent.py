from logic import *
from utils import *
from exploration import *

#import time to test performance
import time
#A knowledge base for a wumpusWorld
class wumpusKB():
    def __init__(self, wumpusWorld):
        self.kb = PropKB()
        #Add in the KB basic information
        
        #No pit and wumpus at (0,0)
        self.kb.tell(expr("~P00"))
        self.kb.tell(expr("~W00"))
        
        #Add the rules of the game
        #If square x,y is breezy <==> (adjacent are pits)
        for i in range(0,4):
            for j in range(0,4):
                head = ("B"+str(i)+str(j))
                p = adjacentRooms(i,j)
                body = "("
                for room in p:
                    body += "P"+str(room[0])+str(room[1])+" | "
                body = body[:-2] + ")"
                #Add the double implication about pits to the kb
#                print(expr(head + " <=> " + body))
                self.kb.tell(expr(head + " <=> " + body))
        #Add rules for wumpus S <=> (adjacent are wumpus)
        for i in range(0,4):
            for j in range(0,4):
                head = ("S"+str(i)+str(j))
                p = adjacentRooms(i,j)
                body = "("
                for room in p:
                   body += "W"+str(room[0])+str(room[1])+" | "
                body = body[:-2] + ")"
#                print(expr(head+ " <=> "+ body))
                #Add the double implication about pits to the kb
                self.kb.tell(expr(head + " <=> " + body))
        #If we have a wumpus, then all adjacent rooms have stench
#        for i in range(0,4):
#                for j in range(0,4):
#                    head = ("W"+str(i)+str(j))
#                    body = "("
#                    for room in adjacentRooms(i,j):
#                        body += "S"+str(room[0])+str(room[1])+" & "
#                    body = body[:-2] + ")"
#                    print(expr(head + " <=> "+body))
#                    self.kb.tell(expr(head + " <=> " + body))
        #If we have pit, then all adjacent rooms have breeze 
#        for i in range(0,4):
#               for j in range(0,4):
#                   head = ("P"+str(i)+str(j))
#                   body = "("
#                   for room in adjacentRooms(i,j):
#                      body += "B"+str(room[0])+str(room[1])+" & "
#                   body = body[:-2] + ")"
#                   print(expr(head + " <=> "+body))
#                   self.kb.tell(expr(head + " <=> " + body))
        #If we dont smell Stench then no wumpus in adjacent rooms
        for i in range(0,4):
                for j in range(0,4):
                    head = ("~S"+str(i)+str(j))
                    body = "("
                    for room in adjacentRooms(i,j):
                        body += "~W"+str(room[0])+str(room[1])+" & "
                    body = body[:-2] + ")"
#                    print(expr(head + " <=> "+body))
                    self.kb.tell(expr(head + " <=> " + body))
        #If we dont feel breeze then no pit in adjacent rooms
        for i in range(0,4):
                for j in range(0,4):
                    head = ("~B"+str(i)+str(j))
                    body = "("
                    for room in adjacentRooms(i,j):
                        body += "~P"+str(room[0])+str(room[1])+" & "
                    body = body[:-2] + ")"
#                    print(expr(head + " <=> "+body))
                    self.kb.tell(expr(head + " <=> " + body))
 


        #There is at least one wumpus
        sentence = "("
        for i in range(0,4):
            for j in range(0,4):
                sentence += "W"+str(i)+str(j)+" | " 
        sentence = sentence[:-2]+")"
        self.kb.tell(expr(sentence))

        #For each pair of locations, one of them must be wumpus free
        #Build a list of the symbols
        wr = []
        for i in range(0,4):
            for j in range(0,4):
                wr.append("W"+str(i)+str(j))
        #For each pair
        for i in range(0,len(wr)-1):
            for j in range(i+1,len(wr)):
                p2 = Symbol(wr[j])
                #Add the sentence that says at least one of them must be wumpus free
                self.kb.tell(expr("~"+wr[i] + " | " + "~"+wr[j]))

        #Build a list of symbols
        self.symbolList = []
        for clause in self.kb.clauses:
            for symbol in prop_symbols(clause):
                if(symbol not in self.symbolList):
                   self.symbolList.append(symbol)



    #Take current percept as a list and update KB
    #[Breeze,Stench,Glitter,Bump,Scream]
    def addPercept(self,percept,x,y):
        newSymbol = []
        #Tell KB we felt BXY or ~BXY (breeze at cell(x,y) )
        if(percept[0] == 0):
            newSymbol.append("~B"+str(x)+str(y))
            #self.kb.tell("~B"+str(x)+str(y))

        else:
            newSymbol.append("B"+str(x)+str(y))
            #self.kb.tell(expr("B"+str(x)+str(y)))
        #Tell KB we felt SXY or ~SXY (Stench at cell(x,y) )
        if(percept[1] == 0):
            newSymbol.append("~S"+str(x)+str(y))
            #self.kb.tell("~S"+str(x)+str(y))
        else:
            newSymbol.append("S"+str(x)+str(y))
            #self.kb.tell(expr("S"+str(x)+str(y)))

        #Tell KB if we saw glitter or not at cell (x,y)
        if(percept[2] == 0):
            newSymbol.append("~G"+str(x)+str(y))
            #self.kb.tell("~G"+str(x)+str(y))
        else:
            newSymbol.append("G"+str(x)+str(y))
            #self.kb.tell("G"+str(x)+str(y))

        #Tell the kb
        for s in newSymbol:
            self.kb.tell(expr(s))

        #Update symbol list
        for s in newSymbol:
            if(expr(s) not in self.symbolList):
                self.symbolList.append(expr(s))


    #Return true if room x,y is safe (no wumpus and no pit)
    def safe(self,x,y):
        #This is the expr we want to test if KB entails
        # ( ~Wxy & ~Pxy )
        safeExpr = expr("~W"+str(x)+str(y)+" & "+"~P"+str(x)+str(y))
        #Tell kb the negation of the expr we want to see if it entails
        self.kb.tell(~safeExpr)

        #Try dpll
        result = dpll(self.kb.clauses,self.symbolList,{})
        #Remove our test safeExpr
        self.kb.retract(~safeExpr)

        #Result = false if there was a contradiction => KB entails our safeExpr
        if(result == False):
            return True
        else:
            return False
  
    #Same as before, except we test if (Pij | Wij) is NOT entailed by KB
    def possiblySafe(self,x,y):
         #This is the expr we want to test if KB entails
         #( Wxy | Pxy)
        safeExpr = expr("W"+str(x)+str(y)+" | "+"P"+str(x)+str(y))
        #Tell kb the negation of the expr we want to see if it entails
        self.kb.tell(~safeExpr)

        #Try dpll
        result = dpll(self.kb.clauses,self.symbolList,{})
        #Remove our test safeExpr
        self.kb.retract(~safeExpr)

        #Result = false if there was a contradiction => KB entails our safeExpr
        #We return the negation of entails, we want to return True if KB DOES NOT entails our expr
        #in other words, kb cannot prove that the square is unsafe
        if(result == False):
            return False
        else:
            return True

