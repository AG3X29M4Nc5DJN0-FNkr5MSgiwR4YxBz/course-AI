from searchdir.node import *
from searchdir.util import *

## This method must implement Breadth-first search (BFS)
## It must return the solution node and the number of visited nodes
def breadthfirst_search(initialState):
    print('BFS------------------------------')
    fringe = Queue()
    nbVisited = 0
    node = Node(initialState)
    if(node.state.isGoal()):
        return node, nbVisited
    fringe.enqueue(node)
    #set are magic
    closed = set()
    while(not fringe.isEmpty()):
        currentNode = fringe.dequeue()
        closed.add(currentNode.state)
        nbVisited = nbVisited + 1
        children = currentNode.expand()
        for child in children:
            #check if child is in closed 
            if(not child.state in closed ):
                if(child.state.isGoal()):
                    return child,nbVisited
                fringe.enqueue(child)
    return -1
