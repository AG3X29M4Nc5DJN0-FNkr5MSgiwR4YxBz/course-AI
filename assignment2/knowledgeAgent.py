from logic import *
from utils import *
from wumpusWorld import *
class wumpusKB():
    def __init__(self, wumpusWorld):
        #Create empty kb
        self.kb = PropKB()
        
        #Add in the KB basic information
        #No pit and wumpus at (0,0)
        self.kb.tell(~Symbol("P00"))
        #self.kb.tell(~Symbol("W00"))

        #Add the rules of the game
        #If square x,y is breezy <==> (adjacent are pits)
        for i in range(0,4):
            for j in range(0,4):
                head = Symbol("B"+str(i)+str(j))
                p = adjacentRooms(i,j)
                body = "("
                for room in p:
                    body += "P"+str(room[0])+str(room[1])+" | "
                body = body[:-2] + ")"
                #Add the double implication about pits to the kb
                print(Expr('<=>',head,body))
                self.kb.tell(Expr('<=>',head,body))
        #Add rules for wumpus (stench)
        #for i in range(0,4):
            for j in range(0,4):
                head = Symbol("S"+str(i)+str(j))
                p = adjacentRooms(i,j)
                body = "("
                for room in p:
                   body += "W"+str(room[0])+str(room[1])+" | "
                body = body[:-2] + ")"
                print(Expr('<=>',head,body))
                #Add the double implication about pits to the kb
                self.kb.tell(Expr('<=>',head,body))


        #There is at least one wumpus
        #sentence = "("
        #for i in range(0,4):
        #    for j in range(0,4):
        #        sentence += "W"+str(i)+str(j)+" | " 
        #sentence = sentence[:-2]+")"
        #print(sentence)
        #self.kb.tell(sentence)

        #For each pair of locations, one of them must be wumpus free
        #Build a list of the symbols
        #wr = []
        #for i in range(0,4):
        #    for j in range(0,4):
        #        wr.append("W"+str(i)+str(j))
        #For each pair
        #for i in range(0,len(wr)-1):
        #    for j in range(i+1,len(wr)):
        #        p1 = Symbol(wr[i])
        #        p2 = Symbol(wr[j])
        #        #Add the sentence that says at least one of them must be wumpus free
        #        self.kb.tell(Expr('|',~p1,~p2))


    #Take current sensation as a list and update KB
    #[Stench,Breeze,Glitter,Bump,Scream]
    def addSensation(self,sensation,x,y):
        #Means adjacent squares are safe!
        if(sensation[0] == 0):
            for r in adjacentRooms(x,y):
                self.kb.tell("~W"+str(r[0])+str(r[1]))
        else:
            sentence = "("
            for r in adjacentRooms(x,y):
                sentence += "W"+str(r[0])+str(r[1]) + " | "
            sentence = sentence[:-2]+")"
            self.kb.tell(sentence)

        if(sensation[1] == 0):
            for r in adjacentRooms(x,y):
                self.kb.tell("~P"+str(r[0])+str(r[1]))
        else:
            sentence = "("
            for r in adjacentRooms(x,y):
                sentence += "P"+str(r[0])+str(r[1]) + " | "
            sentence = sentence[:-2]+")"
            self.kb.tell(sentence)
        
        if(sensation[2] == 0):
            self.kb.tell("~G"+str(x)+str(y))
        else:
            self.kb.tell("G"+str(x)+str(y))

    #Return true if room x,y is safe (no wumpus and no pit)
    #Use resolution rule
    def safe(self,x,y):
        pit = Symbol("P"+str(x)+str(y))
        wumpus = Symbol("W"+str(x)+str(y))
        print(pl_resolution(self.kb,~pit))
        print(pl_resolution(self.kb,~wumpus))
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
        

world = wumpusWorld()
wKB = wumpusKB(world)

world.printRoom()
wKB.addSensation(world.sensation,world.aPos[0],world.aPos[1])

print(wKB.kb.clauses)

print(wKB.safe(0,1))
