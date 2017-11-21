from utils import *
from logic import *
import random
from knowledgeAgent import *
from exploration import *

#check performance
import time
#for logging
import sys


class agent():
    def __init__(self,x,y,wumpusWorld):
        self.position = [x, y]
        self.orientation = "r"
        self.score = 0
        self.finalScore = 0
        self.carrying = [1, 0] # index 0 is arrow, 1 is goooold
        self.percept = [0, 0, 0, 0, 0]
        self.kb = wumpusKB(wumpusWorld)
        self.plan = Stack()
        self.terminated = False

        #position used to simulate pathing
        self.simulationOrientation = 'r'
        #Fringe used to explore
        #Our agent will try to explore the safe one first
        self.safeFringe = set()
        self.possiblySafeFringe = set()
        self.unsafeFringe = set()
        self.closed_set = set()

        #Agent first update its initial percept
        self.updatePercept(wumpusWorld)


        #Stats for agent
        self.startTime = time.clock()
        self.movement = 0

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
                and wumpusWorld.r[self.position[0] + 1][self.position[1]].wumpus:
            self.percept[1] = "Stench"

        # if the room doesn't end at the left and there is a pit add breeze
        elif self.position[0] > 0 \
                and wumpusWorld.r[self.position[0] - 1][self.position[1]].wumpus:
            self.percept[1] = "Stench"

        # if the room doesn't end at the bottom and there is a pit add breeze
        elif self.position[1] > 0 \
                and wumpusWorld.r[self.position[0]][self.position[1] - 1].wumpus:
            self.percept[1] = "Stench"

        # if the room doesn't end at the top and there is a pit add breeze
        elif self.position[1] < 3 \
                and wumpusWorld.r[self.position[0]][self.position[1] + 1].wumpus:
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
    
    #Smart agent using A*
    #Our heuristic is simple : if a cell is proved safe its more likely to be the goal
    #When called, it will do one action
    def smartAgent(self, wumpusWorld):
        #If we see gold, we pick it up next thing
        if(self.percept[2]):
            return self.performAction("grab_object",wumpusWorld)
        #Create a cell starting at current position
        currentCell = nodeCell(self.position)
        #Start by telling the kb its percept at current position
        #if we are at a new cell
        if(tuple(self.position) not in self.closed_set):
            self.kb.addPercept(self.percept,self.position[0],self.position[1])
            
            #Whenever we add info to the kb, try to see if we can move nodes from possiblySafe
            #To safe fringe
            #To save time, only do it if we have empty safe fringe
            if(len(self.safeFringe) == 0):
                toRemove = []
                for ele in self.possiblySafeFringe:
                    if(self.kb.safe(ele[0],ele[1])):
                        #Its safe now, remove it from possiblySafe and put it in safeFringe
                        self.safeFringe.add(ele)
                        toRemove.append(ele)
                #Cant remove element during iteration of a set
                for ele in toRemove:
                    self.possiblySafeFringe.remove(ele)


            #expand current cell (get neighbors)
            neighbors = adjacentRooms(self.position[0],self.position[1])
            for n in neighbors:
                r = tuple(n)
                #if n is new position
                if r not in self.safeFringe and r not in self.possiblySafeFringe and \
                r not in self.unsafeFringe and r not in self.closed_set:
                    #add it to the right fringe
                    #Check if its safe
                    if(self.kb.safe(n[0],n[1])):
                        self.safeFringe.add(r)
                    elif(self.kb.possiblySafe(n[0],n[1])):
                        self.possiblySafeFringe.add(r)
                    else:
                        self.unsafeFringe.add(r)

            
            self.closed_set.add(tuple(self.position))

        #If plan is empty
        if len(self.plan) == 0:
 
            #Try to remove a safe node
            #Make a plan for it
            if(len(self.safeFringe) > 0):
                nextPosition = self.safeFringe.pop()
            #if we can't, try to take a possiblySafe node and see if they are proved safe right now
            elif(len(self.possiblySafeFringe) > 0):
                nextPosition = self.possiblySafeFringe.pop()
                #TODO maybe try to find and kill wumpus
            else:
                #TODO try to kill wumpus
                nextPosition = self.unsafeFringe.pop()
            
            self.plan = makePlan(tuple(self.position),self.orientation,tuple(nextPosition),self.closed_set)
        #Now we either created a new plan or we already had one
        #Get next step from plan
        action = self.plan.pop(0)
        #Perform action
        self.performAction(action,wumpusWorld)

    def dumbAgent(self, wumpusWorld):
        # performs actions at random

        if self.percept[2]: # if there is glitter
            self.performAction('grab_object', wumpusWorld)
        elif self.percept[1] and self.carrying[0] == 1: # if there is a stench and still has arrow
            self.performAction('fire_arrow', wumpusWorld)
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
        self.movement += 1
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
            self.score -= 1
            oldX = self.position[0]
            oldY = self.position[1]
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
                if self.position[0] > 0:  # if the x position of the agent is smaller than 3
                    self.position = [self.position[0] - 1, self.position[1]]
                else:
                    bump=True

            elif self.orientation == 'd':
                if self.position[1] > 0:  # if the y position of the agent is smaller than 3
                    self.position = [self.position[0], self.position[1]-1]
                else:
                    bump=True
            #Tell world we moved to cell x,y
            #TODO I don't see how better we can make that be ...
            wumpusWorld.moveAgent(self.position[0], self.position[1])
            #If the current location after moving is dangerous...we lose
            if(wumpusWorld.isDanger(self.position[0],self.position[1])):
                    self.score -= 1000
                    self.endTime = time.clock()
                    self.terminated = True
        # the agent will try to grab an object
        # if there is nothing, nothing happens
        # if the gold is there it should add it to its inventory
        elif action == 'grab_object':
            if wumpusWorld.r[self.position[0]][self.position[1]].gold:
                self.carrying[1] = "Gold"
                self.score += 1000
                #If we grab gold the simulation finish
                self.endTime = time.clock()
                self.terminated = True


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
                    wumpusWorld.killWumpus()  # kill the wumpus, the stenches will
                    # be updated next percept update

            elif self.orientation == 'l':
                # wumpus must be to the left of the agent and in the same row
                if wumpusWorld.wX < self.position[0] and wumpusWorld.wY == self.position[1]:
                    scream = True
                    wumpusWorld.killWumpus()  # kill the wumpus, the stenches will
                    # be updated next percept update

            elif self.orientation == 'u':
                # wumpus must be up of the agent and in the same column
                if wumpusWorld.wY > self.position[1] and wumpusWorld.wX == self.position[0]:
                    scream = True
                    wumpusWorld.killWumpus()  # kill the wumpus, the stenches will
                    # be updated next percept update

            elif self.orientation == 'd':
                # wumpus must be up of the agent and in the same column
                if wumpusWorld.wY < self.position[1] and wumpusWorld.wX == self.position[0]:
                    scream = True
                    wumpusWorld.killWumpus()  # kill the wumpus, the stenches will
                    # be updated next percept update

        self.updatePercept(wumpusWorld, bump, scream)
    #Print agent status
    def status(self):
        if(self.terminated):
            print("[-] AGENT TERMINATED")
            print("SCORE : " + str(self.score))
            print("Movement : " + str(self.movement))
            print("TIME  : " + str(self.endTime - self.startTime))
            self.finalScore = self.score
            #Flush stdout so we can see it in the log.txt file
            sys.stdout.flush()
        else:
            print("[+] Agent status")
            print("[+] Current position (x,y) : "+str(self.position[0]) + ","+str(self.position[1]))
            print("[+] Current direction      : "+str(self.orientation))
            print("[+] Current score          : "+str(self.score))
            print("[+] Current percept        : "+str(self.percept))


