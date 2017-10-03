from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    fringe = Stack()
    node = Node(initialState)
    fringe.push(node)
    closed = []
    while(not fringe.isEmpty()):
        currentNode = fringe.pop()
        if (currentNode.isGoal()):
            return currentNode
        listActions = currentNode.possibleActions()
        children = []
        #Create a new node, make the action and add the children list
        for a in listActions:
            #Copy node, make action then store in stack
            childNode = EightPuzzleState(currentNode.configuration)
            childNode.executeAction(a)
            children.append(childNode)
        
        closed.append(currentNode)
        for node in children:
            if(node not in closed and node not in fringe):
                fringe.push(node)
