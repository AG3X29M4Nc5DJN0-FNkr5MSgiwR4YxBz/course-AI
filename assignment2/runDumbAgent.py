from wumpusWorld import *
from agent import *

flag = input("Please type 0 to run default simulation or anything else to run a random world: ")

if flag == '0':
    # Set the world
    # #world#0 - original simulation
    w0 = wumpusWorld()

    # overwrites the rooms created by the constructor for the test
    for i in range(0, 4):
        for j in range(0, 4):
            w0.r[i][j] = room()

    # resets the rooms to the default configuration
    w0.r[2][0].pit = True
    w0.r[0][2].wumpus = True
    w0.r[1][2].gold = True
    w0.r[2][2].pit = True
    w0.r[3][3].pit = True
    w0.r[0][0].agent = True

    # create the agent
    a = agent(0, 0, w0)
    while (not a.terminated):  # run until agent died or picked up gold
        w0.printRoom()
        a.status()
        a.dumbAgent(w0)
    a.status()
    w0.printRoom()
else:
    #create a random world
    w = wumpusWorld()
    # create the agent
    a = agent(0, 0, w)
    while (not a.terminated):  # run until agent died or picked up gold
        w.printRoom()
        a.status()
        a.dumbAgent(w)
    a.status()
    w.printRoom()
