## Author: Amal Zouaq
### azouaq@uottawa.ca
### Author: Hadi Abdi Ghavidel
###habdi.cnlp@gmail.com

from operator import attrgetter
import unittest

# :)
class unitTest(unittest.TestCase):
    def testQueue(self):
        testQueue = Queue()
        
        self.assertEqual(testQueue.isEmpty(),True)

        #Test enqueue and dequeue
        testQueue.enqueue("Bonjour")
        testQueue.enqueue("test1")
        testQueue.enqueue("test2")

        poped1 = testQueue.dequeue()
        poped2 = testQueue.dequeue()

        self.assertEqual(poped1,"Bonjour")
        self.assertEqual(poped2,"test1")
        #Test show and size
        current = testQueue.show()
        size = len(current)
        self.assertEqual(size,1)
        #Test contains
        self.assertEqual("test2" in testQueue,True)
        self.assertEqual("test1" in testQueue,False)

        self.assertEqual(testQueue.isEmpty(),False)

    def testpQueue(self):
        testpQueue = PriorityQueue(lambda x : len(x))

        self.assertEqual(testpQueue.isEmpty(),True)
        #Test enqueue and dequeue
        testpQueue.enqueue("min chat")
        testpQueue.enqueue("ptit chat")
        testpQueue.enqueue("moyen chat")
        testpQueue.enqueue("gros gros chat")

        poped1 = testpQueue.dequeue()
        poped2 = testpQueue.dequeue()

        self.assertEqual(poped1,"gros gros chat")
        self.assertEqual(poped2,"moyen chat")

        #Test show and size
        current = testpQueue.show()
        size = len(current)
        self.assertEqual(size,2)

        #test contains
        self.assertEqual("min chat" in testpQueue,True)
        self.assertEqual("faux chat" in testpQueue,False)
        self.assertEqual(testpQueue.isEmpty(),False)

    def testStack(self):
        testStack = Stack()
        self.assertEqual(testStack.isEmpty(),True)
        #Test push and pop
        testStack.push(1)
        testStack.push(2)
        testStack.push(3)
        testStack.push(99)
        testStack.push(213)

        poped1 = testStack.pop()
        poped2 = testStack.pop()

        self.assertEqual(poped1,213)
        self.assertEqual(poped2,99)

        #Test show and size
        current = testStack.show()
        size = len(current)
        self.assertEqual(size,3)
        #test contains
        self.assertEqual(3 in testStack,True)
        self.assertEqual(5 in testStack,False)
        self.assertEqual(testStack.isEmpty(),False)
        
#Queue - Implementation of the data structure Queue
class Queue:
    # initializes the current data structure
    def __init__(self):
        self.queue = []

    # returns the elements of the current data structure
    def show(self):
        return self.queue
    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        if(len(self.queue) == 0):
            return True
        return False

    # add the element item to the current data structure
    def enqueue(self, item):
        self.queue.append(item)

    # removes an element from the current data structure
    def dequeue(self):
        return self.queue.pop(0)

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.queue)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
        if item in self.queue:
            return True
        return False


#Priority Queue Implementation of the data structure PriorityQueue
class PriorityQueue:
    # initializes the data structure
    def __init__(self, fct):
        #use dictionaries
        self.pQueue = {}
        self.fct = fct

    # returns the elements of the current data structure
    def show(self):
        return self.pQueue

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        if (len(self.pQueue) == 0):
            return True
        return False

    # add the element item to the current data structure
    #TODO is that the right way to do it? Should we sort first or not?
    def enqueue(self, item):
    #We decided to add it to the dictionary and not sort it.
    #less complexity when queueing, more when dequeueing
    #TODO verify when does python think two items are the same?
        self.pQueue[item] = self.fct(item)
    # removes an element from the current data structure
    def dequeue(self):
        maxScore = 0
        #find the item with max score
        for item,score in self.pQueue.items():
            if (maxScore < score):
                result = item
        #Delete it
        del self.pQueue[result]
        return result

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.pQueue)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
        if item in self.pQueue:
            return True
        return False

#Stack - Implementation of the data structure Stack
class Stack:
    # initializes the data structure
    def __init__(self):
        self.stack = []
    # returns the elements of the current data structure
    def show(self):
        return self.stack
    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        if (len(self.stack) == 0):
            return True
        return False
    # add the element item to the current data structure
    def push(self, item):
        self.stack.append(item)

    # removes an element from the current data structure
    def pop(self):
        return self.stack.pop()

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.stack)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
        if item in self.stack:
            return True
        return False


#Prints results for search alorithms
def printResults(alg, solution, start, stop, nbvisited):
    try:
        result, depth = solution.extractSolutionAndDepth()
        if result != []:
            print("The Solution is  ", (result))
            print("The Solution is at depth ", depth)
            print("The path cost is ", solution.getcost())
            print('Number of visited nodes:', nbvisited)
            time = stop - start
            print("The execution time is ", time, "seconds.")
            print("Done!")
    except AttributeError:
        print("No solution")
    except MemoryError:
        print("Memory Error!")

if __name__=='__main__':
    unittest.main()
