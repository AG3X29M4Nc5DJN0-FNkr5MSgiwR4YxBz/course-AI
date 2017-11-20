from utils import *
from logic import *
from util import *
from node import *
import random
from knowledgeAgent import *

class agent():
    def __init__(self,x,y,wumpusWorld):
        self.position = [x, y]
        self.orientation = "r"
        self.score = 0
        self.carrying = [1, 0] # index 0 is arrow, 1 is goooold
        self.percept = [0, 0, 0, 0, 0]
        self.kb = wumpus_kb(wumpusWorld)
        self.plan = []
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
                       'grab_object': 1}

        if agent.carrying[0] == 1:
            temp_action['fire_arrow'] = 1

        return temp_action

    def dumbAgent(self, wumpusWorld):
        # performs actions at random

        if self.percept[2]: # if there is glitter
            self.performAction('grab_object', wumpusWorld)
        elif self.percept[1] and self.carrying[0]: # if there is a stench and still has arrow
            self.performAction('fire_arrow')
        else:  # perform random movement action
            selector = random.randint(0, 2)
            choices = ['turn_left', 'turn_right', 'move_forward']
            choice = choices[selector]
            self.performAction(choice, wumpusWorld)

        # performActions automatically updates the percepts with the
        # bumps and scream and everything.

    def performAction(self, action, wumpusWorld):
        # if action is to turn left, it will update the orientation
        # and percepts shouldnt change
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
        # if action is to turn right, it will update the orientation
        # and percepts shouldnt change
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
        # the agent will try to move forward in the direction it is currently facing
        # if there is a wall, the bump percept is added
        elif action == 'move_forward':
            bump = False
            self.score -= 1
            if self.orientation == 'r':
                if self.position[0] < 3:  # if the x position of the agent is smaller than 3
                    self.position = [self.position[0]+1, self.position[1]]
                else:
                    bump=True

            elif self.orientation == 'u':
                if self.position[1] < 3:  # if the y position of the agent is smaller than 3
                    self.position = [self.position[0], self.position[1]+1]
                else:
                    bump=True

            elif self.orientation == 'l':
                if self.position[1] < 3:  # if the y position of the agent is smaller than 3
                    self.position = [self.position[0] - 1, self.position[1]]
                else:
                    bump=True

            elif self.orientation == 'd':
                if self.position[1] < 3:  # if the y position of the agent is smaller than 3
                    self.position = [self.position[0], self.position[1]-1]
                else:
                    bump=True
        # the agent will try to grab an object
        # if there is nothing, nothing happens
        # if the gold is there it should add it to its inventory
        elif action == 'grab_object':
            self.score -= 1
            if wumpusWorld.r[self.position[0], self.position[1]].gold:
                self.carrying[1] = "Gold"
                self.score += 1001

        # the agent will fire an arrow if it still is carrying one
        # if the wumpus is facing the agent, the wumpus will die and
        # get removed from the world, im not sure if the stenches are
        # removed too
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

    # def expandAction(self, initial, actions):
    #     # returns a list of possible outcomes for every possible actions
    #
    #     # initial is a list containing a position and an orientation like so:
    #     possible_states = []
    #     pos = initial[0]  # pos is a list of x and y ; ex: [0, 1]
    #     ori = initial[1]  # ori is a letter depicting which direction the agent
    #                       # is facing
    #     # get a list of all possible actions in i
    #     for i in actions.items():
    #         temp_pos = pos  # get a temporary position and orientation
    #         temp_ori = ori
    #
    #         # we check for every movement action and if it is valid
    #         if i[0] == 'turn_left' and i[1]:
    #             if ori == 'r':
    #                 temp_ori = 'u'  # change temp to the proper orientation
    #             elif ori == 'u':
    #                 temp_ori = 'l'
    #             elif ori == 'l':
    #                 temp_ori = 'd'
    #             else:
    #                 temp_ori = 'r'
    #             # now we push the new configuration into the new possible_state list
    #             # we need to keep track of the position, orientation and the action taken
    #             # to be able to create a sequence of actions later on
    #             possible_states.append(temp_pos, temp_ori, 'turn_left')
    #         if i[0] == 'turn_right' and i[1]:
    #             if ori == 'r':
    #                 temp_ori = 'd'
    #             elif ori == 'd':
    #                 temp_ori = 'l'
    #             elif ori == 'l':
    #                 temp_ori = 'u'
    #             else:
    #                 temp_ori = 'r'
    #             possible_states.append(temp_pos, temp_ori, 'turn_right')
    #         if i[0] == 'move_forward' and i[1]:
    #             if ori == 'r' and pos[0] < 3:
    #                 temp_pos = [temp_pos[0]+1, temp_pos[1]]
    #             elif ori == 'd' and pos[1] > 0:
    #                 temp_pos = [temp_pos[0], temp_pos[1]-1]
    #             elif ori == 'l' and pos[0] > 0:
    #                 temp_pos = [temp_pos[0]-1, temp_pos[1]]
    #             elif ori == 'u' and pos[1] < 3:
    #                 temp_pos = [temp_pos[0], temp_pos[1]+1]
    #             possible_states.append(temp_pos, temp_ori, 'move_forward')
    #     return possible_states
    #
    # # this method is supposed to be the one doing exploration to find out
    # # the best sequence of action to do ...
    # def whichAction(self, wumpusWorld):  # hybrid wumpus agent method
    #     self.kb.tell(self.updatePercept(wumpusWorld))
    #
    #     # get the adjacent rooms to where the agent is
    #     adjRooms = adjacentRooms(self.position[0], self.position[1])
    #     safe_frontier = []
    #     unsafe_frontier = []
    #     visited = [[0, 0]]
    #
    #     for i in range(len(adjRooms)):
    #         if i not in visited not in safe_frontier not in unsafe_frontier:
    #             if self.kb.safe(i[0], i[1]):
    #                 safe_frontier.append(i)
    #             else:
    #                 unsafe_frontier.append(i)
    #
    # def pathPlanning(self, goal_cell):
    #     fringe = Stack()
    #     closed = set()
    #     init_state = [self.position, self.orientation, ""]
    #     fringe.push(init_state)
    #     while not fringe.isEmpty():
    #         currentNode = fringe.pop()
    #         if currentNode[0] == goal_cell:
    #             return currentNode[2]
    #         closed.add(currentNode)
    #         children = self.expandAction([currentNode[0], currentNode[1]], self.possibleActions())
    #         for node in children:
    #             if node not in closed or node not in fringe:
    #                 node[2] += currentNode
