### Author: Amal Zouaq
### azouaq@uottawa.ca
## Author: Hadi Abdi Ghavidel
## habdi.cnlp@gmail.com

import timeit

if __name__=='__main__':
    #If we run the testcases add syspath to fix imports
    import sys
    sys.path.append("./../../")

import numpy as np
import random
from searchdir.blindSearch.breadthfirst_search import *
from searchdir.blindSearch.depthfirst_search import *
from searchdir.heuristicSearch.astar_search import *
from searchdir.state import *
# import unittest
#
# class unitTest(unittest.TestCase):
#
#     def testEightPuzzleState(self):
#         #Make test state
#         print("Test creating states")
#         goal = EightPuzzleState([0,1,2,3,4,5,6,7,8])
#         state1 = EightPuzzleState([8,4,3,2,5,0,6,7,1])
#         state2 = EightPuzzleState([4,7,6,1,2,5,8,0,3])
#         state3 = EightPuzzleState([1,0,2,3,4,5,6,7,8])
#         print("test printing goal state")
#         goal.show()
#
#         print("test printing state3")
#         state3.show()
#         #Test if we can detect goal
#         self.assertEqual(goal.isGoal(), True)
#         self.assertEqual(state2.isGoal(), False)
#         #Test possibleActions
#         #In state3 1 0 2
#         #          3 4 5
#         #          6 7 8
#         #There are 3 possibles actions : move left, move right or move down
#         #Thus actions is
#         action = [0,1,3]
#         possibleAction = state3.possibleActions()
#         self.assertEqual(action,possibleAction)
#
#         #Test move down on state3
#         print("move down")
#         c = state3.executeAction(action[2])
#         c.show()
#         expected = EightPuzzleState([1,4,2,3,0,5,6,7,8])
#         self.assertEqual(state3.configuration,expected.configuration)
#         #Test move left on new state3
#         #In state3  1 4 2
#         #           3 0 5
#         #           6 7 8
#         print("move left")
#         action = [0,1,2,3]
#         possibleAction = c.possibleActions()
#         self.assertEqual(action,possibleAction)
#         print("***")
#         c.show()
#         c1 = c.executeAction(action[0])
#         c.show()
#         print("***")
#         expected = EightPuzzleState([1,4,2,0,3,5,6,7,8])
#         #test equals()
#         self.assertEqual(state3.equals(expected.configuration),True)
#
#         #Test heuristics
#         closeState = EightPuzzleState([1,0,2,3,4,5,6,7,8])
#         farState =   EightPuzzleState([8,7,6,5,4,3,2,1,0])
#
#         h1 = closeState.heuristic1()
#         h1Far = farState.heuristic1()
#         h1Goal = goal.heuristic1()
#         self.assertEqual(h1,2)
#         self.assertEqual(h1Far,8)
#         self.assertEqual(h1Goal,0)
#
# #       h2 = closeState.heuristic2()
# #       h2Far = farState.heuristic2()
# #       h1Goal = goal.heuristic()
#
#
#
# #        self.assertEqual(h2Goal,0)
#
#
class EightPuzzleState(State):

    #initializes the eight puzzle with the configuration passed in parameter (numbers)
    def __init__(self, numbers):
        self.configuration = numbers  #initializes the array of tiles 0 will represent the empty tile


    #returns a boolean value that indicates if the current configuration is the same as the goal configuration
    def isGoal(self):
        if self.configuration == [0,1,2,3,4,5,6,7,8]:
            return True
        else:
            return False

    # returns the set of legal actions in the current state
    #In the list, 0 = left, 1 = right, 2 = up and 3 = down
    def possibleActions(self):
        actions = []
        # four possible actions at most and at least two
        index0 = self.configuration.index(0)
        if index0 != 0 and index0 != 3 and index0 != 6:
            # empty tile is not in first column and can thus move to the left
            actions.append(0)

        if index0 != 2 and index0 != 5 and index0 != 8:
            # empty tile is not in third column and can thus move to the right
            actions.append(1)

        if index0 >= 3:
            # empty tile is not in first row and can thus move to the top
            actions.append(2)

        if index0 <= 5:
            # empty tile is not in last row and can thus move to the bottom
            actions.append(3)

        return actions


    # applies the result of the move on the current state
    def executeAction(self, move):
        #TODO can we do something less hard coded?
        #TODO apply it on current state - remove child
        child = EightPuzzleState(self.configuration)
        index0 = child.configuration.index(0)
        #move left
        if(move == 0):
            assert(index0 != 0 and index0 != 3 and index0 != 6)
            tempValue = child.configuration[index0-1]
            #Exchange values
            child.configuration[index0] = tempValue
            child.configuration[index0-1] = 0
        #move right
        elif(move == 1):
            assert(index0 != 2 and index0 != 5 and index0 != 8)
            tempValue = child.configuration[index0+1]
            #Exchange values
            child.configuration[index0] = tempValue
            child.configuration[index0+1] = 0
        #move up
        elif(move == 2):
            assert(index0 >= 3)
            tempValue = child.configuration[index0-3]
            #Exchange values
            child.configuration[index0] = tempValue
            child.configuration[index0-3] = 0
        #move down
        elif(move == 3):
            assert(index0 <= 5)
            tempValue = child.configuration[index0+3]
            #Exchange values
            child.configuration[index0] = tempValue
            child.configuration[index0+3] = 0
        return child
    # returns true if the current state is the same as other, false otherwise
    # other must be a list
    def equals(self, other):
        return self.configuration == other
    
    # prints the grid representing the current state
    # e.g. -----------
        # | 0 | 1 | 2 |
        # -----------
        # | 3 | 4 | 5 |
        # -----------
        # | 6 | 7 | 8 |
        # -----------
    def show(self):
        print(' -----------')  # prints first line of dashes

        i = 0
        while i < 3:
            print("| " + str(self.configuration[i]) + " ", end="")
            i += 1
        print("|")
        print(' -----------')  # prints last line of dashes

        while i < 6:
            print("| " + str(self.configuration[i]) + " ", end="")
            i += 1
        print("|")
        print(' -----------')  # prints last line of dashes

        while i < 9:
            print("| " + str(self.configuration[i]) + " ", end="")
            i += 1
        print("|")
        print(' -----------')  # prints last line of dashes

    # returns the cost of the action in parameter
    def cost(self, action):
        return 1

    # returns the value of the heuristic for the current state
    # note that you can alternatively call heuristic1() and heuristic2() to test both heuristics with A*
    def heuristic(self):
        return self.heuristic1()
        # return self.heuristic2()


    ## returns the value of your first heuristic for the current state
    # make sure to explain it clearly in your comment

    # returns the amount of wrongly placed tiles in the puzzle
    def heuristic1(self):
        goal = [0,1,2,3,4,5,6,7,8]
        heuristic1 = 0
        i = 0
        while i < 9:
            if self.configuration[i] != goal[i]:  # if the value at the same index is not the same, means they
                heuristic1 += 1                   # at the wrong place
            i = i + 1
        return heuristic1


    # returns the value of your first heuristic for the current state
    # make sure to explain it clearly in your comment
    def heuristic2(self, matrix, goal):
        # TO COMPLETE
        return -1

    def __eq__(self,other):
        return self.configuration == other.configuration

####################### SOLVABILITY ###########################

def issolvable(puzzle):
    puzzle_str = np.array(list(map(int, puzzle)))
    print("Puzzle string: ", puzzle_str)
    if inversions(puzzle_str) % 2:
        return False
    else : return True

def inversions(s):
    k = s[s != 0]
    return sum(
        len(np.array(np.where(k[i + 1:] < k[i])).reshape(-1))
        for i in range(len(k) - 1)
    )

def randomize(puzzle):
    puzzle = puzzle.shuffle_ran(puzzle, 1)
    puzzle_choice = []
    for sublist in puzzle.cells:
        for item in sublist:
            puzzle_choice.append(item)
    return puzzle, puzzle_choice

def shuffle_ran(self,board, moves):
        newState = board
        if moves==100:
            return newState
        else:
            newState.executeAction(random.choice(list(board.possibleActions())))
            moves= moves+1
            return self.shuffle_ran(newState, moves)
#Run unit test first
#unittest.main()
#######  SEARCH ###########################
EIGHT_PUZZLE_DATA = [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 0, 2, 3, 4, 5, 8, 7, 6],
                     [4, 0, 6, 1, 2, 8, 7, 3, 5],
                     [1, 2, 8, 7, 3, 4, 5, 6, 0],
                     [5, 1, 3, 4, 0, 2, 7, 6, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [4, 6, 0, 7, 2, 8, 3, 1, 5]]

puzzle_choice = EIGHT_PUZZLE_DATA[6]
puzzle = EightPuzzleState(puzzle_choice)
#puzzle, puzzle_choice = randomize(puzzle)
print('Initial Config')
puzzle.show()
if not issolvable(puzzle_choice):
    print("NOT SOLVABLE")
else:
    start = timeit.default_timer()
    solution, nbvisited = breadthfirst_search(puzzle)
    stop = timeit.default_timer()
    printResults('BFS', solution, start, stop, nbvisited)


    # start = timeit.default_timer()
    # solution, nbvisited = depthfirst_search(puzzle)
    # stop = timeit.default_timer()
    # printResults('DFS', solution, start, stop, nbvisited)

    start = timeit.default_timer()
    solution, nbvisited = astar_search(puzzle)
    stop = timeit.default_timer()
    printResults('A*', solution, start, stop, nbvisited)

