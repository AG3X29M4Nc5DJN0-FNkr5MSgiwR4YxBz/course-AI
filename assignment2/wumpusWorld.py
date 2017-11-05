import random
class wumpusWorld():
    #The wumpus world is represented by a 4x4 matrix
    #Coordinates start from bottom left
    #  (0,3)...(3,3)
    #  (0,2)...(3,2)
    #  (0,1)...(3,1)
    #  (0,0)...(3,0)
    room = [[0] * 4 for i in range(4)] 
    #Create a new wumpus world
    def __init__(self):
        #Place the wumpus, can never be at 1,1
        wX = 0
        wY = 0
        while(wX == 0 and wY == 0):
            wX = random.randint(0,3)
            wY = random.randint(0,3)
        self.room[wX][wY] = 'W'

        #Place the gold
        tX = wX
        tY = wY
        while((tX == wX and tY == wY) or
              (tX == 0 and tY == 0)):
            tX = random.randint(0,3)
            tY = random.randint(0,3)
        self.room[tX][tY] = 'G'

        #Generate pits
        for i in range(0,4):
            for j in range(0,4):
                if(self.room[i][j] == 0):
                    pit = random.random()
                    if(pit < 0.2):
                        self.room[i][j] = 'P'
        #Make sure no pit at 0,0
        self.room[0][0] = 0

        #Initial agent configuration
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
            roomList.append(self.room[x-1][y])
        if(x < 3):
            roomList.append(self.room[x+1][y])
        if(y > 0):
            roomList.append(self.room[x][y-1])
        if(y < 3):
            roomList.append(self.room[x][y+1])
        for r in roomList:
            #Stench
            if(r == 'W'):
                sensation[0] = "Stench"
            elif(r == 'P'):
                sensation[1] = "Breeze"
        if(self.room[x][y] == 'G'):
            sensation[2] = "Glitter"
        return sensation


    def printRoom(self):
        for j in range(3,-1,-1):
            for i in range(0,4):
                print(str(self.room[i][j]), end=' ')
            print('',end='\n')
    #returns a boolean value that indicates if the current configuration is the same as the goal configuration
    #def isGoal(self):
    #def possibleActions(self):
    #def executeAction(self, move):
    #def equals(self, other):
    #def cost(self, action):

w = wumpusWorld()
w.printRoom()
