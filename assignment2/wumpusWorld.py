import random

class room():
    def __init__(self):
        self.pit = False
        self.wumpus = False
        self.gold = False
        self.agent = False
    def __str__(self):
        s = "["
        if(self.pit):
            s+= "P"
        if(self.wumpus):
            s+= "W"
        if(self.gold):
            s+= "G"
        if(self.agent):
            s+= "A"
        s+= "]"
        return s

class wumpusWorld():
    #The wumpus world is represented by a 4x4 matrix
    #Coordinates start from bottom left
    #  (0,3)...(3,3)
    #  (0,2)...(3,2)
    #  (0,1)...(3,1)
    #  (0,0)...(3,0) 
    #Create a new wumpus world
    def __init__(self):
        #Create rooms
        self.r = []
        for i in range(0,4):
            self.r.append([])
            for j in range(0,4):
                self.r[i].append(room())
        #Place the wumpus, can never be at 1,1
        wX = 0
        wY = 0
        while(wX == 0 and wY == 0):
            wX = random.randint(0,3)
            wY = random.randint(0,3)
        self.r[wX][wY].wumpus = True

        #Place the gold
        #can never be on the wumpus
        tX = wX
        tY = wY
        while((tX == wX and tY == wY) or
              (tX == 0 and tY == 0)):
            tX = random.randint(0,3)
            tY = random.randint(0,3)
        self.r[tX][tY].gold = True

        #Generate pits
        for i in range(0,4):
            for j in range(0,4):
                if(self.r[i][j].wumpus == False and
                   self.r[i][j].gold == False):
                    pit = random.random()
                    if(pit < 0.2):
                        self.r[i][j].pit = True
        #Make sure no pit at 0,0
        self.r[0][0].pit = False

        #Initial agent configuration
        self.r[0][0].agent = True
        self.aPos = [0,0]
        self.aDir = 'r'

        self.sensation = self.getSensation(0,0)
        print(self.sensation)

    #Sensation felt by the agent
    #[Stench,Breeze,Glitter,Bump,Scream]
    #Return a sensation array for the room at x,y
    def getSensation(self,x,y):
        sensation = [0,0,0,0,0]
        #Determine directly adjacent room
        roomList = []
        if(x > 0):
            roomList.append(self.r[x-1][y])
        if(x < 3):
            roomList.append(self.r[x+1][y])
        if(y > 0):
            roomList.append(self.r[x][y-1])
        if(y < 3):
            roomList.append(self.r[x][y+1])
        for r in roomList:
            #Stench
            if(r.wumpus):
                sensation[0] = "Stench"
            elif(r.pit):
                sensation[1] = "Breeze"
        if(self.r[x][y].gold):
            sensation[2] = "Glitter"
        return sensation


    def printRoom(self):
        for j in range(3,-1,-1):
            for i in range(0,4):
                print(str(self.r[i][j]), end=' ')
            print('',end='\n')

    #def isGoal(self):
    #def possibleActions(self):
    #def executeAction(self, move):
    #def equals(self, other):
    #def cost(self, action):

w = wumpusWorld()
w.printRoom()
