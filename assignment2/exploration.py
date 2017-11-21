#To test performance
import time

#quickly made bfs with  #Return a list of actions to go from currentPosition
#To goal position (given by goal : [x,y])
#Moving only throught already visited cells (cells in closed_set)
#TODO fix if we take as parameters obj or []
def makePlan(currentPosition,currentOrientation,goal,visitedNodeSet):
    plan = []
    simulationOrientation = currentOrientation
    start = time.clock()
    currentCell = findGoalBFS(currentPosition,goal,visitedNodeSet)
    end = time.clock()
    print("Time spend in BFS to find path to goal : " + str(end-start))
    #From the goal cell, build in a list the trail of position
    trail = [currentCell.position]
    while(currentCell.previous != None):
        trail.insert(0,currentCell.previous.position)
        currentCell = currentCell.previous

    #From trail, build plan
    #Check first element of the trail, it should be our current position
    assert(trail[0] == currentPosition)
    #Now, for each next cell, we should be able to go to it
    for i in range(0,len(trail)-1):
        #For each pair, we add to plan the path to go from one to the other
        r = pathAdjacentPosition(trail[i],trail[i+1],simulationOrientation)
        #Append new path
        plan += r[0] 
        #Change our simulationDirection
        simulationOrientation = r[1]
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

#quickly made bfs with cell class
#return the goal cell with .previous containing the path
def findGoalBFS(initialPosition,goal,visitedNodeSet): 
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
            if(child.position not in closed and child.position in visitedNodeSet):
                pFringe.insert(0,child)

#Return a list of actions to go from one adjacent position to the other  
def pathAdjacentPosition(p0,p1,simulationOrientation):
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
    while(not(simulationOrientation == desiredDirection)):
        simulationOrientation = rotateDirectionRight(simulationOrientation)
        plan.append("turn_right")
    #Now move forward
    plan.append("move_forward")
    return plan,simulationOrientation

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
 
