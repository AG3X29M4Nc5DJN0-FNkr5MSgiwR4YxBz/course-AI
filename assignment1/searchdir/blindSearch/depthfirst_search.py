from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    fringe = Stack()
    fringe.push(initialState)
    closed = []
    while(not fringe.isEmpty()):
        currentNode = fringe.pop()
        #TODO what is solution node : to implement?
        if (currentNode == solutionNode):
            return currentNode
        #TODO modify to fit the nodeclass
        children = currentNode.generate
        closed.append(currentNode)
        for node in children:
            if(node not in closed and node not in fringe):
                fringe.push(node)
