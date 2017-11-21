from utils import *
from logic import *
from node import *
import random
from knowledgeAgent import *
from exploration import *

#check performance
import time

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

        #For astar_agent create a priorityQueue
        #3 possibles values : 0 = safe, 1 = possibly safe and 2 = unsafe
        #our astar will always try to visit safe cell first (h = askSafe)
      #  self.fringe = PriorityQueue(order=min,f=agent.cellScore)
      #  self.closed_set = set()
        #position used to simulate pathing
        self.simulationOrientation = 'r'

        self.safeFringe = []
        self.possiblySafeFringe = []
        self.unsafeFringe = []
        self.closed_set = [] 

        #Agent first update its initial percept
        self.updatePercept(wumpusWorld)

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
    def astar_Agent(self, wumpusWorld):
        start0 = time.clock()
        #Create a cell starting at current position
        currentCell = nodeCell(self.position)
        #Start by telling the kb its percept at current position
        #if we are at a new cell
        if(self.position not in self.closed_set):
            start = time.clock()
            print("adding to kb "+str(self.position))
            self.kb.addPercept(self.percept,self.position[0],self.position[1])

            #Whenever we add info to the kb, try to see if we can move nodes from possiblySafe
            #To safe fringe
            for ele in self.possiblySafeFringe:
                if(self.kb.safe(ele[0],ele[1])):
                   #Its safe now, remove it from possiblySafe and put it in safeFringe
                   self.safeFringe.append(ele)
                   self.possiblySafeFringe.remove(ele)

            #expand current cell (get neighbors)
            neighbors = adjacentRooms(self.position[0],self.position[1])
            for n in neighbors:
                #if n is new position
                if n not in self.safeFringe and n not in self.possiblySafeFringe and \
                n not in self.unsafeFringe and n not in self.closed_set:
                    #add it to the right fringe
                    #Check if its safe
                    if(self.kb.safe(n[0],n[1])):
                        self.safeFringe.append(n)
                    elif(self.kb.possiblySafe(n[0],n[1])):
                        self.possiblySafeFringe.append(n)
                    else:
                        self.unsafeFringe.append(n)
            self.closed_set.append(self.position)
            end = time.clock()
            print("Time spend in the expand neighbors of unexplored cells : " +str(end-start))

        #If we see gold, we pick it up next thing
        if(self.percept[2]):
            self.plan.insert(0,"grab_object")

        #print("current orientation :")
        #print(self.orientation)
        #print("current plan :")
        #print(self.plan)

        #If plan is empty
        if len(self.plan) == 0:
 
            print("Safe fringe :")
            for ele in self.safeFringe:
                print(str(ele))
            print("PossiblySafe :")
            for ele in self.possiblySafeFringe:
                print(str(ele))
            print("Unsafe :")
            for ele in self.unsafeFringe:
                print(str(ele))
            print("Closed :")
            for ele in self.closed_set:
                print(str(ele))
            
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
            
            #When dequeued from fringe, add it to closed_set (visited cells)
            #TODO test it
            #self.closed_set.append(nextCell)
            print("Choosed to move to : " +str(nextPosition))
            self.plan = makePlan(self.position,self.orientation,nextPosition,self.closed_set)
        #Now we either created a new plan or we already had one
        #Get next step from plan
        action = self.plan.pop(0)
        #Perform action
        self.performAction(action,wumpusWorld)
        end0 = time.clock()
        print("Time spend in 1 iteration of astar : "+str(end0-start0))



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
            #TODO improve this
            wumpusWorld.moveAgent(oldX,oldY,self.position[0], self.position[1])
            #If the current location after moving is dangerous...we lose
            if(wumpusWorld.isDanger(self.position[0],self.position[1])):
                    self.score -= 1000
                    self.terminated = True
        # the agent will try to grab an object
        # if there is nothing, nothing happens
        # if the gold is there it should add it to its inventory
        elif action == 'grab_object':
            if wumpusWorld.r[self.position[0]][self.position[1]].gold:
                self.carrying[1] = "Gold"
                self.score += 1000
                #If we grab gold the simulation finish
                self.terminated = True


        # the agent will fire an arrow if it still is carrying one
        # if the wumpus is facing the agent, the wumpus will die and
        # get removed from the world, im not sure if the stenches are
        # removed too
        elif action == 'fire_arrow':
            if wumpusWorld.wX is None or wumpusWorld.wY is None:
                self.score -= 10
                print("NO ARROW")
                return
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
            self.finalScore = self.score
        else:
            print("[+] Agent status")
            print("[+] Current position (x,y) : "+str(self.position[0]) + ","+str(self.position[1]))
            print("[+] Current direction      : "+str(self.orientation))
            print("[+] Current score          : "+str(self.score))
            print("[+] Current percept        : "+str(self.percept))

