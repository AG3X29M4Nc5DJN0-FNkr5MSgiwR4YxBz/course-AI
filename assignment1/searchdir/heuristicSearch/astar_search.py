
from operator import attrgetter
from searchdir.node import *
from searchdir.util import PriorityQueue

## This method must implement A* search
## It must return the solution node and the number of visited nodes
def astar_search(initialState):
    print('A* ------------------------------------')
    open_set = PriorityQueue(lambda node: node.f)
    initial_node = Node(initialState, cost=0)
    open_set.enqueue(initial_node)
    closed_set = set()
    nb_visited = 0

    while open_set.isEmpty() is False:
        current = open_set.dequeue()
        if current.state.isGoal() is True:
            print("Goal is found")
            return current, nb_visited
        closed_set.add(current.state)
        for neighbors in current.expand():
            nb_visited += 1
            cost = current.g + 1  # assuming 1 since all moves have a cost of 1
            if neighbors in open_set and cost < neighbors.g:
                open_set.dequeue()
            if neighbors.state in closed_set and cost < neighbors.g:  # should not need this if heuristic is consistent
                closed_set.remove(neighbors)
            if neighbors not in open_set and neighbors.state not in closed_set:
                open_set.enqueue(neighbors)
