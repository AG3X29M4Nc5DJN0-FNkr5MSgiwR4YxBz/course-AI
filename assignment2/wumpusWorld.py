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
    # def __init__(self):
    #     self.r = []
    #     for i in range(0, 4):
    #         self.r.append([])
    #         for j in range(0, 4):
    #             self.r[i].append(room())
    #     # Place the agent ,always at 0,0
    #     self.r[0][0].agent = True
    #
    #     # place the wumpus at 0,2
    #     self.wX = 0
    #     self.wY = 2
    #     self.r[0][2].wumpus = True
    #
    #     # generate the gold at 1,2
    #     self.r[1][2].gold = True
    #
    #     # place the pits 0, 2; 2,2; 3,3
    #     self.r[0][2].pit = True
    #     self.r[2][2].pit = True
    #     self.r[3][3].pit = True
    #
    #     # Initial agent configuration
    #     self.r[0][0].agent = True
    #     self.aPos = [0, 0]
    #     self.aDir = 'r'
    #
    #     self.percept = self.getPercept(0, 0)
    #     print(self.percept)

    #TODO to test actual wumpusWorld, uncomment this method and comment the one above
    def __init__(self):
        #Create rooms
        self.r = []
        for i in range(0,4):
            self.r.append([])
            for j in range(0,4):
                self.r[i].append(room())
        #Place the agent ,always at 0,0
        self.r[0][0].agent = True


        #Place the wumpus, can never be at 1,1
        self.wX = 0
        self.wY = 0
        while(self.wX == 0 and self.wY == 0):
            self.wX = random.randint(0,3)
            self.wY = random.randint(0,3)
        self.r[self.wX][self.wY].wumpus = True

        #Place the gold
        #can never be on the wumpus
        tX = self.wX
        tY = self.wY
        while((tX == self.wX and tY == self.wY) or
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

        self.percept = self.getPercept(0,0)
        print(self.percept)

    #percept felt by the agent
    #[Stench,Breeze,Glitter,Bump,Scream]
    #Return a percept array for the room at x,y
    def getPercept(self,x,y):
        percept = [0,0,0,0,0]
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
                percept[0] = "Stench"
            elif(r.pit):
                percept[1] = "Breeze"
        if(self.r[x][y].gold):
            percept[2] = "Glitter"
        return percept


    def printRoom(self):
        for j in range(3,-1,-1):
            for i in range(0,4):
                print(str(self.r[i][j]), end=' ')
            print('',end='\n')
    #Move an agent from a space to another
    def moveAgent(self,oldX,oldY,x,y):
        self.r[oldX][oldY].agent = False
        self.r[x][y].agent = True

    def moveWumpus(self,oldX,oldY,x,y): # used for tests
        self.r[oldX][oldY].wumpus = False
        self.r[x][y].wumpus = True
        self.wX = x
        self.wY = y
    #Return if the current cell is dangerous
    def isDanger(self,x,y):
        if(self.r[x][y].wumpus == True or self.r[x][y].pit == True):
            return True
        else:
            return False

    def killWumpus(self):
        self.r[self.wX][self.wY].wumpus = False
        self.wX = None
        self.wY = None
    # def wumpusAlive(self):
    #     return self.r[self.wX][self.wY].wumpus

    #def isGoal(self):
    #def possibleActions(self):
    #def executeAction(self, move):
    #def equals(self, other):
    #def cost(self, action):


#w = wumpusWorld()
#w.printRoom()
