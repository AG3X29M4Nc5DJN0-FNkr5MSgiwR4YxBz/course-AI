### Author: Amal Zouaq
### azouaq@uottawa.ca
## Author: Hadi Abdi Ghavidel
## habdi.cnlp@gmail.com

import timeit

if __name__=='__main__':
    #If we run the testcases add syspath to fix imports
    import sys
    sys.path.append("../../")

import numpy as np
import random
from searchdir.blindSearch.breadthfirst_search import *
from searchdir.blindSearch.depthfirst_search import *
from searchdir.heuristicSearch.astar_search import *
from searchdir.state import *
import unittest

class unitTest(unittest.TestCase):

    def testEightPuzzleState(self):
        #Make test state
        print("Test creating states")
        goal = EightPuzzleState([0,1,2,3,4,5,6,7,8])
        state1 = EightPuzzleState([8,4,3,2,5,0,6,7,1])
        state2 = EightPuzzleState([4,7,6,1,2,5,8,0,3])
        state3 = EightPuzzleState([1,0,2,3,4,5,6,7,8])
        print("test printing goal state")
        goal.show()

        #Test if we can detect goal
        self.assertEqual(goal.isGoal(), True)
        self.assertEqual(state2.isGoal(), False)
        #Test possibleActions
        #In state3 1 0 2
        #          3 4 5
        #          6 7 8
        #There are 3 possibles actions : move left, move down or move right
        #Thus actions is
        action = [0,2,-1,4]
        possibleAction = state3.possibleActions()
        self.assertEqual(action,possibleAction)


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
    # the set of legal movements are confined in a list, the list has always 4 of length
    # the first position represents the new empty position to the left, -1 if impossible
    # the second position represents the new empty position to the right, -1 if impossible
    # the third position represents the new empty position to the top, -1 if impossible
    # the fourth position represents the new empty position to the bottom, -1 if impossible

    def possibleActions(self):
        actions = []
        # four possible actions at most and at least two
        test = self.configuration.index(0) - 1
        if test != -1 or 2 or 5:
            # empty tile is not in first column and can thus move to the left
            actions.append(test)
        else:
            actions.append(-1)  # insert invalid move for left movement

        test = self.configuration.index(0) + 1
        if test != 3 or 6 or 9:
            # empty tile is not in third column and can thus move to the right
            actions.append(test)
        else:
            actions.append(-1)  # insert invalid move for right movement

        test = self.configuration.index(0) - 3
        if test >= 0:
            # empty tile is not in first row and can thus move to the top
            actions.append(test)
        else:
            actions.append(-1)  # insert invalid move for top movement

        test = self.configuration.index(0) + 3
        if test <= 8:
            # empty tile is not in first row and can thus move to the bottom
            actions.append(test)
        else:
            actions.append(-1)  # insert invalid move for bottom movement

        return actions


    # applies the result of the move on the current state
    def executeAction(self, move):
        # Here, we have to switch the index of the empty tile with the tile at the new empty tile
        # I suspect there is going to be a method to chose which direction the empty tile is going to move
        # so I assume that move is a number taken from the possibleActions return statement

        tempValue = self.configuration.index(move)  # store the value of the tile before it becomes empty
        self.configuration[self.configuration.index('0')] = tempValue  # place that value where the old empty tile was
        self.configuration[move] = 0  # place the new empty tile

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
        while i > 9:
            if self.configuration[i] != goal[i]:  # if the value at the same index is not the same, means they
                heuristic1 += 1                   # at the wrong place


    # returns the value of your first heuristic for the current state
    # make sure to explain it clearly in your comment
    def heuristic2(self, matrix, goal):
        # TO COMPLETE
        return -1


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
unittest.main()
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


    start = timeit.default_timer()
    solution, nbvisited = depthfirst_search(puzzle)
    stop = timeit.default_timer()
    printResults('DFS', solution, start, stop, nbvisited)

    start = timeit.default_timer()
    solution, nbvisited = astar_search(puzzle)
    stop = timeit.default_timer()
    printResults('A*', solution, start, stop, nbvisited)

