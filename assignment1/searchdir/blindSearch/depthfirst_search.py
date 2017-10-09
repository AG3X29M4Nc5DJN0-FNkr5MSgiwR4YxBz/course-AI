
from searchdir.node import *
from searchdir.util import *


## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    fringe = Stack()
    node = Node(initialState)
    fringe.push(node)
    nb_visited = 0
    closed = set()
    while(not fringe.isEmpty()):
        currentNode = fringe.pop()
        if (currentNode.state.isGoal()):
            return currentNode, nb_visited
        closed.add(currentNode.state)
        children = currentNode.expand()
        nb_visited += 1
        for node in children:
            if(not(node.state in closed or node in fringe)):
                fringe.push(node)
