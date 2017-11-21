# Wumpus propositionnal Agent
Assignment 2 of CSI4106

## File description
### agent.py
Contains the code of the smart agent (using uniform cost search), of the dumbAgent.
This is also the file where we finds functions to update the percept of the agent, make him
actions and print his status
### knowledgeAgent.py
Contains the code of the knowledge base. This is where the code of the wumpus_kb is found.
Wumpus_kb is a class containing a propKB from aima_python, the methods of this class allow you to add
We also used dpll from aima-python to do inference on the knowledge base
percepts to the kb and infer if cells are safe
### exploration.py
Contains the code to explore wumpus world, get adjacent rooms from a given position, make a plan from
one room to another, do a BFS to find the path
### wumpus_world.py
Define a wumpus world as a matrix of rooms.
Contains functions to interact with the world, such as getting the percept at a certain room, move the agent 
and print the state of each rooms
### logic.py, agents.py and utils.py
Code taken from aima-python (https://github.com/aimacode/aima-python) an open-source library. They implement algorithms found in the book "Artificial Intellienge - A modern Approach" by Russel and Norvig's
logic.py contains implementation of propositionnal logic
utils.py contains utilities such as PriorityQueue implementations
agents.py contains implementation of agents (unused directly in our code)
### runDumbAgent.py and runSmartAgent.py
main file to run a smart or a dumb agent.
Execute with python3 filename and it will run multiple simulations
