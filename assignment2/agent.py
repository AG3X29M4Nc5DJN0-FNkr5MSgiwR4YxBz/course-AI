from knowledgeAgent import *

class agent():
    def __init__(self,x,y):
        self.position = [x, y]
        self.orientation = "r"
        self.score = 0
        self.carrying = [1, 0] # index 0 is arrow, 1 is goooold
        self.percept = [0, 0, 0, 0, 0]
    def updatePercept(self, wumpusWorld, bump=False, scream=False):
        # bump and scream are going to be boolean values


        # update the breeze percept
        self.percept[0] = 0
        # if the room doesn't end at the right and there is a pit add breeze

        if self.position[0] < 3 \
                and wumpusWorld.r[self.position[0] + 1][self.position[1]].pit:
            self.percept[0] = "Breeze"

        # if the room doesn't end at the left and there is a pit add breeze
        elif self.position[0] > 0 \
                and wumpusWorld.r[self.position[0] - 1][ self.position[1]].pit:
            self.percept[0] = "Breeze"

        # if the room doesn't end at the bottom and there is a pit add breeze
        elif self.position[1] > 0 \
                and wumpusWorld.r[self.position[0]][ self.position[1] - 1].pit:
            self.percept[0] = "Breeze"

        # if the room doesn't end at the top and there is a pit add breeze
        elif self.position[1] < 3 \
                and wumpusWorld.r[self.position[0]][ self.position[1] + 1].pit:
            self.percept[0] = "Breeze"

        # check for wumpus
        self.percept[1] = 0
        #pretty much same strategy as the breeze, I decided to split the if
        #statement to make it easier to read the code
        if self.position[0] < 3 \
                and wumpusWorld.r[self.position[0] + 1][ self.position[1]].wumpus:
            self.percept[1] = "Stench"

        # if the room doesn't end at the left and there is a pit add breeze
        elif self.position[0] > 0 \
                and wumpusWorld.r[self.position[0] - 1][ self.position[1]].wumpus:
            self.percept[1] = "Stench"

        # if the room doesn't end at the bottom and there is a pit add breeze
        elif self.position[1] > 0 \
                and wumpusWorld.r[self.position[0]][ self.position[1] - 1].wumpus:
            self.percept[1] = "Stench"

        # if the room doesn't end at the top and there is a pit add breeze
        elif self.position[1] < 3 \
                and wumpusWorld.r[self.position[0]][ self.position[1] + 1].wumpus:
            self.percept[1] = "Stench"


        #now, the GOOOOLD
        self.percept[2] = 0
        if wumpusWorld.r[self.position[0]][ self.position[1]].gold:
            self.percept[2] = "Glitter"

        # for the bump
        self.percept[3] = 0
        if bump:
            self.percept[3] = "Bump"

        # for the scream
        self.percept[4] = 0
        if scream:
            self.percept[4] = "Scream"

    def possibleActions(self):
        temp_action = {'turn_left': 1,
                       'turn_right': 1,
                       'move_forward': 1,
                       'fire_arrow': 0,
                       'grab_object': 0}

        if agent.carrying[0] == 1:
            temp_action['grab_object'] = 1

    def performAction(self, action, wumpusWorld):
        bump = False
        scream = False
        if action == 'turn_left':
            self.score -= 1
            if self.orientation == 'r':
                self.orientation = 'u'
            elif self.orientation == 'u':
                self.orientation = 'l'
            elif self.orientation == 'l':
                self.orientation = 'd'
            else:
                self.orientation = 'r'

        elif action == 'turn_right':
            self.score -= 1
            if self.orientation == 'r':
                self.orientation = 'd'
            elif self.orientation == 'd':
                self.orientation = 'l'
            elif self.orientation == 'l':
                self.orientation = 'u'
            else:
                self.orientation = 'r'
        elif action == 'move_forward':
            bump = True
            self.score -= 1
            if self.orientation == 'r':
                if self.position[0] < 3:  # if the x position of the agent is smaller than 3
                    self.position = [self.position[0]+1, self.position[1]]
                else:
                    bump=True

            if self.orientation == 'u':
                if self.position[1] < 3:  # if the y position of the agent is smaller than 3
                    self.position = [self.position[0], self.position[1]+1]
                else:
                    bump=True

            if self.orientation == 'l':
                if self.position[0] > 0:  # if the x position of the agent is greater than 0
                    self.position = [self.position[0] - 1, self.position[1]]
                else:
                    bump=True

            if self.orientation == 'd':
                if self.position[1] > 0:  # if the y position of the agent is greater than 0
                    self.position = [self.position[0], self.position[1]-1]
                else:
                    bump=True

        elif action == 'grab_object':
            self.score -= 1
            if wumpusWorld.r[self.position[0], self.position[1].gold]:
                self.carrying[1] = "Gold"
                self.score += 1001

        elif action == 'fire_arrow':
            self.score -= 10
            self.carrying[0] = 0
            if self.orientation == 'r':
                # wumpus must be to the right of the agent and in the same row
                if wumpusWorld.wX > self.position[0] and wumpusWorld.wY == self.position[1]:
                    scream = True
                    wumpusWorld.r[wumpusWorld.wX, wumpusWorld.wY].wumpus = False  # kill the wumpus, the stenches will
                    # be updated next percept update

            elif self.orientation == 'l':
                # wumpus must be to the left of the agent and in the same row
                if wumpusWorld.wX < self.position[0] and wumpusWorld.wY == self.position[1]:
                    scream = True
                    wumpusWorld.r[wumpusWorld.wX, wumpusWorld.wY].wumpus = False  # kill the wumpus, the stenches will
                    # be updated next percept update

            elif self.orientation == 'u':
                # wumpus must be up of the agent and in the same column
                if wumpusWorld.wY > self.position[1] and wumpusWorld.wX == self.position[0]:
                    scream = True
                    wumpusWorld.r[wumpusWorld.wX, wumpusWorld.wY].wumpus = False  # kill the wumpus, the stenches will
                    # be updated next percept update

            elif self.orientation == 'd':
                # wumpus must be up of the agent and in the same column
                if wumpusWorld.wY < self.position[1] and wumpusWorld.wX == self.position[0]:
                    scream = True
                    wumpusWorld.r[wumpusWorld.wX, wumpusWorld.wY].wumpus = False  # kill the wumpus, the stenches will
                    # be updated next percept update

        self.updatePercept(wumpusWorld, bump, scream)

    def isCurrentCellGoal(self, wumpusWorld):
        if self.carrying[1]:
            return True
        else:
            return False
