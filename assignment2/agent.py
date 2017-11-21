from utils import *
from logic import *
from node import *
import random
from knowledgeAgent import *


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

        currentCell = nodeCell(self.position)
        #Start by telling the kb its percept at current position
        #if we are at a new cell
        if(currentCell not in self.closed_set):
            self.kb.addPercept(self.percept,self.position[0],self.position[1])
            #Create a cell starting at current position

            #expand current cell (get neighbors)
            neighbors = currentCell.expand() 
            for n in neighbors:
                #if n is new cell
                if n not in self.safeFringe and n not in self.possiblySafeFringe and \
                n not in self.unsafeFringe and n not in self.closed_set:
                    #add it to the right fringe
                    print("adding : ")
                    print(n.position)
                    #Check if its safe
                    if(self.kb.safe(n.position[0],n.position[1])):
                        self.safeFringe.append(n)
                    elif(self.kb.possiblySafe(n.position[0],n.position[1])):
                        self.possiblySafeFringe.append(n)
                    else:
                        self.unsafeFringe.append(n)
            self.closed_set.append(currentCell)

        #If we see gold, we pick it up next thing
        if(self.percept[2]):
            self.plan.insert(0,"grab_object")

        print("Safe fringe :")
        for ele in self.safeFringe:
            print(str(ele.position))
        print("PossiblySafe :")
        for ele in self.possiblySafeFringe:
            print(str(ele.position))
        print("Unsafe :")
        for ele in self.unsafeFringe:
            print(str(ele.position))
        print("Closed :")
        for ele in self.closed_set:
            print(str(ele.position))

        #print("current orientation :")
        #print(self.orientation)
        #print("current plan :")
        #print(self.plan)

        #If plan is empty
        if len(self.plan) == 0:
            #Try to remove a safe node
            #Make a plan for it
            if(len(self.safeFringe) > 0):
                nextCell = self.safeFringe.pop()
                print("removing : ")
                print(nextCell.position)
            #if we can't, try to take a possiblySafe node
            elif(len(self.possiblySafeFringe) > 0):
                nextCell = self.possiblySafeFringe.pop()
                #TODO maybe try to find and kill wumpus
            else:
                #TODO try to kill wumpus
                nextCell = self.unsafeFringe.pop()
            
            #When dequeued from fringe, add it to closed_set (visited cells)
            #TODO test it
            #self.closed_set.append(nextCell)
            print("Choosed to move to : " +str(nextCell.position))
            self.plan = self.makePlan(nextCell.position)
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

    #Return a list of actions to go from currentPosition
    #To goal position (given by goal : [x,y])
    #Moving only through already visited cells (cells in closed_set)
    #TODO fix if we take as parameters obj or []
    def makePlan(self, goal):
        plan = []
        self.simulationOrientation = self.orientation
        currentCell = self.findGoalBFS(self.position,goal)
        #From the goal cell, build in a list the trail of position
        trail = [currentCell.position]
        while(currentCell.previous != None):
            trail.insert(0,currentCell.previous.position)
            currentCell = currentCell.previous

        #From trail, build plan
        #Remove first element of the trail, it should be our current position
        assert(trail[0] == self.position)
        #Now, for each next cell, we should be able to go to it
        for i in range(0,len(trail)-1):
            #For each pair, we add to plan the path to go from one to the other
            plan += self.pathAdjacentPosition(trail[i],trail[i+1])
        return(plan)
    #return 0 if safe
    #return 1 if possibly safe
    #return 2 if unsafe
    def cellScore(self,node):
        if(self.kb.safe(node.position[0],node.position[1])):
            return 0
        elif(self.kb.possiblySafe(node.position[0],node.position[1])):
            return 1
        else:
            return 2
    #Return a list of actions to go from one adjacent position to the other  
    def pathAdjacentPosition(self,p0,p1):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        #First, check that the distance between the two position is 1
        dX = abs(x1-x0)
        dY = abs(y1-y0)
        plan = []
        assert(dX+dY == 1)
        #Now, check the direction we should face
        if(x1 > x0):
            desiredDirection = 'r'
        elif(y1 > y0):
            desiredDirection = 'u'
        elif(y0 > y1):
            desiredDirection = 'd'
        else:
            desiredDirection = 'l'
    
        #Calculate the action to do to be in the right direction
        #TODO improve if we have time
        #While we dont face the right wait, turn right until we do
        while(not(self.simulationOrientation == desiredDirection)):
            self.simulationOrientation = rotateDirectionRight(self.simulationOrientation)
            plan.append("turn_right")
        #now we just need to move forward
        plan.append("move_forward")
        return plan

    #quickly made bfs with cell class
    #return the goal cell with .previous containing the path
    def findGoalBFS(self,initialPosition,goal): 
        pFringe = []
        node = nodeCell(initialPosition)
        goal = nodeCell(goal)
        #If we are already at the goal, return empty plan
        if(node == goal):
            return node 
        pFringe.insert(0,(node))
        closed = [] 
        while(len(pFringe) > 0):
            currentNode = pFringe.pop()
            closed.append(currentNode.position)
            children = currentNode.expand()
            for child in children:
                if(child.position == goal.position):
                    return child
                #If its not goal and not already visited by our agent, we dont explore
                if(child.position not in closed and child in self.closed_set):
                     pFringe.insert(0,child)

    #quickly made bfs with cell class
    #return the goal cell with .previous containing the path
    def findGoalBFS(self,initialPosition,goal):
        pFringe = []
        node = nodeCell(initialPosition)
        goal = nodeCell(goal)
         #If we are already at the goal, return empty plan
        if(node == goal):
            return node
        pFringe.insert(0,(node))
        closed = []
        while(len(pFringe) > 0):
            currentNode = pFringe.pop()
            closed.append(currentNode.position)
            children = currentNode.expand()
            for child in children:
                #If child is not already visited in our BFS
                if(child.position not in closed):
                    if(child.position == goal.position):
                        return child
                    #If its not goal and not already visited by our agent, we dont explore
                    if(child.position not in closed and child not in self.closed_set):
                        pFringe.insert(0,child)

    #Return a list of actions to go from one adjacent position to the other
    def pathAdjacentPosition(self,p0,p1):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        #First, check that the distance between the two position is 1
        dX = abs(x1-x0)
        dY = abs(y1-y0)
        plan = []
        assert(dX+dY == 1)
        #Now, check the direction we should face
        if(x1 > x0):
            desiredDirection = 'r'
        elif(y1 > y0):
            desiredDirection = 'u'
        elif(y0 > y1):
            desiredDirection = 'd'
        else:
            desiredDirection = 'l'

        #Calculate the action to do to be in the right direction
        #TODO improve if we have time
        #While we dont face the right wait, turn right until we do
        while(not(self.simulationOrientation == desiredDirection)):
            self.simulationOrientation = rotateDirectionRight(self.simulationOrientation)
            plan.append("turn_right")
        #now we just need to move forward
        plan.append("move_forward")
        return plan

#Take a direction as char and return the direction if we turn right
def rotateDirectionRight(direction):
    if(direction == 'r'):
        return 'd'
    elif(direction == 'd'):
        return 'l'
    elif(direction == 'l'):
        return 'u'
    elif(direction == 'u'):
        return 'r'

#return 0 if safe
#return 1 if possibly safe
#return 2 if unsafe
def cellScore(kb,node):
    if(kb.safe(node.position[0],node.position[1])):
        return 0
    elif(kb.possiblySafe(node.position[0],node.position[1])):
        return 1
    else:
        return 2

#Node object for makeplan search
class nodeCell():
    def __init__(self,position):
        self.position = position
        self.previous = None

    #Since nodeCell are cells, we can use the adjacentRoom function
    def expand(self):
        adjacentPosition = adjacentRooms(self.position[0],self.position[1])
        cellList = []
        for p in adjacentPosition:
            newCell = nodeCell(p)
            newCell.previous = self
            cellList.append(newCell)
        return cellList
    def __eq__(self,other):
        if(other == None):
            return False
        return self.position == other.position
