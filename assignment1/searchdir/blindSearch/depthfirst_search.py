
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
    nb_visited = 0
    while(not fringe.isEmpty()):
        currentNode = fringe.pop()
        if (currentNode.state.isGoal()):
            return currentNode, nb_visited
        listActions = currentNode.state.possibleActions()
        nb_visited += 1
        children = []
        #Create a new node, make the action and add the children list
        for a in listActions:
            #Copy node, make action then store in stack
            childNode = Node(currentNode.state.executeAction(a))
            children.append(childNode)
        closed.append(currentNode)
        for node in children:
            if(node not in closed and node not in fringe):
                fringe.push(node)
