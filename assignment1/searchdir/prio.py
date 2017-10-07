import state

class PriorityQueue:
    def __init__(self):
        self.queue = []  # contains nodes

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    # method the enqueue the nodes in the priorityqueue, we will not be sorting by insertion
    def enqueue(self, node):
        self.queue.append(node)

    def dequeue(self):
        if self.is_empty() is True:
            print("Priority Queue is empty ! Cannot dequeue anything from it.")
            return 0
        else:  # queue is not empty, let's proceed
            best_node = self.queue[0]
            del self.queue[0]
            for index, nodes in enumerate(self.queue):
                if nodes.f < best_node.f:
                    self.queue.append(best_node)  # place back the node that is not the best anymore inside the queue
                    best_node = nodes  # new node takes the place of the best
                    del self.queue[index]  # which in turns, needs to be deleted from the queue
        return best_node

    def size(self):
        return len(self.queue)

    def __contains__(self, item):
        if item in self.queue:
            return True
        else:
            return False
