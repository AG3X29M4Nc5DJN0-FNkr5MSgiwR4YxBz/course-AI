from logic import *
from utils import *
from wumpusWorld import *
class wumpusKB():
    def __init__(self, wumpusWorld):
        #Create empty kb
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
                print(expr(head + " <=> " + body))
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
                print(expr(head+ " <=> "+ body))
                #Add the double implication about pits to the kb
                self.kb.tell(expr(head + " <=> " + body))
        #If we have a wumpus, then all adjacent rooms have stench
      #  for i in range(0,4):
      #          for j in range(0,4):
      #              head = ("W"+str(i)+str(j))
      #              body = "("
      #              for room in adjacentRooms(i,j):
      #                  body += "S"+str(room[0])+str(room[1])+" & "
      #              body = body[:-2] + ")"
      #              print(expr(head + " <=> "+body))
      #              self.kb.tell(expr(head + " <=> " + body))
        #If we have pit, then all adjacent rooms have breeze 
      #  for i in range(0,4):
      #         for j in range(0,4):
      #             head = ("P"+str(i)+str(j))
      #             body = "("
      #             for room in adjacentRooms(i,j):
      #                body += "B"+str(room[0])+str(room[1])+" & "
      #             body = body[:-2] + ")"
      #             print(expr(head + " <=> "+body))
      #             self.kb.tell(expr(head + " <=> " + body))
        #If we dont smell Stench then no wumpus in adjacent rooms
        for i in range(0,4):
                for j in range(0,4):
                    head = ("~S"+str(i)+str(j))
                    body = "("
                    for room in adjacentRooms(i,j):
                        body += "~W"+str(room[0])+str(room[1])+" & "
                    body = body[:-2] + ")"
                    print(expr(head + " <=> "+body))
                    self.kb.tell(expr(head + " <=> " + body))
        #If we dont feel breeze then no pit in adjacent rooms
        for i in range(0,4):
                for j in range(0,4):
                    head = ("~B"+str(i)+str(j))
                    body = "("
                    for room in adjacentRooms(i,j):
                        body += "~P"+str(room[0])+str(room[1])+" & "
                    body = body[:-2] + ")"
                    print(expr(head + " <=> "+body))
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

    #Take current percept as a list and update KB
    #[Breeze,Stench,Glitter,Bump,Scream]
    def addPercept(self,percept,x,y):
        #If we dont smell Stench, adjacents squares are safe
        if(percept[0] == 0):
            self.kb.tell("~B"+str(x)+str(y))
        else:
            self.kb.tell(expr("B"+str(x)+str(y)))
        
        if(percept[1] == 0):
            self.kb.tell("~S"+str(x)+str(y))
        else:
            self.kb.tell(expr("S"+str(x)+str(y)))


        if(percept[2] == 0):
            self.kb.tell("~G"+str(x)+str(y))
        else:
            self.kb.tell("G"+str(x)+str(y))

    #Return true if room x,y is safe (no wumpus and no pit)
    def safe(self,x,y):
        #This is the expr we want to test if KB entails
        safeExpr = expr("~W"+str(x)+str(y)+" & "+"~P"+str(x)+str(y))
        #Tell kb the negation of the expr we want to see if it entails
        self.kb.tell(~safeExpr)

        clauseList = self.kb.clauses
        #build symbol list
        s = []
        for clause in clauseList:
            for symbol in prop_symbols(clause):
                if(symbol not in s):
                    s.append(symbol)
        #Try dpll
        result = dpll(clauseList,s,{})
        #Remove our test safeExpr
        self.kb.retract(~safeExpr)
  #      for key in result.keys():
  #        print(str(key) + " : " + str(result[key]))
        #Result = false if there was a contradiction => KB entails our safeExpr
        if(result == False):
            return True
        else:
            return False
    #Same as before, except we test if (Pij | Wij) is NOT entails
    def possiblySafe(self,x,y):
         #This is the expr we want to test if KB entails
        safeExpr = expr("W"+str(x)+str(y)+" | "+"P"+str(x)+str(y))
        #Tell kb the negation of the expr we want to see if it entails
        self.kb.tell(~safeExpr)

        clauseList = self.kb.clauses
        #build symbol list
        s = []
        for clause in clauseList:
            for symbol in prop_symbols(clause):
                if(symbol not in s):
                    s.append(symbol)
        #Try dpll
        result = dpll(clauseList,s,{})
        #Remove our test safeExpr
        self.kb.retract(~safeExpr)
        #for key in result.keys():
        #   print(str(key) + " : " + str(result[key]))
        #Result = false if there was a contradiction => KB entails our safeExpr
        if(result == False):
            return False
        else:
            return True


#Return a list of adjacent rooms in the form [x,y]
def adjacentRooms(x,y):
    r = []
    if(x > 0):
        r.append([x-1,y])
    if(x < 3):
        r.append([x+1,y])
    if(y > 0):
        r.append([x,y-1])
    if(y < 3):
        r.append([x,y+1])
    return r
        

#world = wumpusWorld()
#wKB = wumpusKB(world)

#world.printRoom()
#wKB.addPercept(world.percept,world.aPos[0],world.aPos[1])

#print(wKB.kb.clauses)
#print("Checking SAFE(0,1) : "+ str(wKB.safe(0,1)))
#print("Checking SAFE(1,0) : "+ str(wKB.safe(1,0)))

#print("Checking possiblySAFE(0,1) : "+str(wKB.possiblySafe(0,1)))
#print("Checking possiblySAFE(1,0) : "+str(wKB.possiblySafe(1,0)))
