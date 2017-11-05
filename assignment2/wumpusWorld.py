### Author: Amal Zouaq
### azouaq@uottawa.ca
## Author: Hadi Abdi Ghavidel
## habdi.cnlp@gmail.com

import timeit

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
        aPos = [0,0]
        aDir = 'r'

        #Sensation in each rooms
        #TODO

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
