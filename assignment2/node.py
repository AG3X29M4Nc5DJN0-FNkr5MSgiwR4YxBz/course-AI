# -*- coding: utf-8 -*-
#
#  Class Node
# This class represents a node in a tree search

import sys
import math
import copy


class Node(object):
    def __init__(self, state, action=None, cost=0, previous=None):
        self.state = state  # state represented by the node
        self.previous = previous  # previous node in the solution path
        self.action = action  # action that resulted in the state represented by the node

    ####################
    # Public methods
    ####################

    # Returns a list of all new nodes that represents next possible states in the exploration
    def expand(self, possibleActions):
        return map(lambda s: self._createNode(s), possibleActions)

    # Check if current node state already exists in path from initial node
    def isRepeated(self):
        return self._findState(self.previous, self.state)
    # Extracts the sequence of states and actions that lead to current node
    def extractSolution(self):
        solution = []
        currentNode = self
        if currentNode is not None:
            while currentNode.previous:
                solution.append(currentNode.action)
                currentNode = currentNode.previous
            solution.reverse()
        return solution


        # Extracts the sequence of states and actions that lead to current node

    def extractSolutionAndDepth(self):
        solution = []
        depth = 0
        currentNode = self
        if currentNode is not None:
            while currentNode.previous:
                solution.append(currentNode.action)
                depth += 1
                currentNode = currentNode.previous
            solution.reverse()
        return solution, depth


    ####################
    # Private methods
    ####################

    def _createNode(self, action):
        newState = copy.deepcopy(self.state)
        newState.executeAction(action)
        return Node(newState, action, self.g + self.state.cost(action), self)

    def _findState(self, node, state):
        if node == None:
            return False
        else:
            if node.state.equals(state):
                return True
            else:
                return self._findState(node.previous, state)
