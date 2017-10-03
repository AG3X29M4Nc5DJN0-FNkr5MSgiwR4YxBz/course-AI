from searchdir.node import *
from searchdir.util import *

## This method must implement Breadth-first search (BFS)
## It must return the solution node and the number of visited nodes
def breadthfirst_search(initialState):
    print('BFS------------------------------')
    fringe = Queue()
    if(initialState.isGoal()):
        return initialState
    fringe.enqueue(initialState)
    explored = []
    while(not fringe.isEmpty()):
        currentNode = fringe.dequeue()
        explored.append(currentNode)
        for action in currentNode.possibleActions():
            child = currentNode.executeAction(action)
            #check if child is in fringe or in explored
            if(not(child in fringe or child in explored)):
                if(child.isGoal()):
                    child.show()
                    return child
                fringe.enqueue(child)
    return -1
