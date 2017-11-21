from wumpusWorld import *
from agent import *
from knowledgeAgent import *

w0 = wumpusWorld()


#Set the world

#for i in range(0,4):
#    for j in range(0,4):
#        w0.r[i][j] = room()

#world#0 - original simulation

#w0.r[2][0].pit = True
#w0.r[0][2].wumpus = True
#w0.r[1][2].gold = True
#w0.r[2][2].pit = True
#w0.r[3][3].pit = True
#w0.r[0][0].agent = True

#World #1

#w0.r[0][1].pit = True
#w0.r[3][0].gold = True
#w0.r[3][2].wumpus = True
#w0.r[0][3].pit = True

#World #2, bug : BFS was going thought unsafe spaces

#w0.r[0][2].wumpus = True
#w0.r[1][1].pit = True
#w0.r[2][3].gold = True
#w0.r[3][2].pit = True

#World #3, bug : KB should've been able to say gold tile was safe
#Bug was : we added the cell to possiblySafe, later on we could've proved it was safe
#But the cell stayed in possiblySafe
#Fix : When added clause to kb, checkc if we can move cell from possibly to safe fringe
#w0.r[2][0].wumpus = True
#w0.r[1][2].pit = True
#w0.r[3][2].gold = True
#w0.r[3][3].pit = True

#Test w0

a = agent(0,0,w0)
while(not a.terminated):
    w0.printRoom()
    a.status()
    a.astar_Agent(w0)

print(a.score)

#scoreTotal = 0
#for i in range(10000):
#    w = wumpusWorld()
#    a = agent(0, 0, w)
#    while(not a.terminated):
#        w.printRoom()
#        a.status()
#        a.astar_Agent(w)
#    a.status()
#    scoreTotal += a.finalScore

#print("Average payoff: {}".format(scoreTotal))
#print(a0.kb.kb.clauses)


#counter = 0
#scoreList = []
#while(counter < 10000):
    #Create a new world
#    w = wumpusWorld()
    #create a new agent
#    a = agent(0,0,w)
    #Do the testDumbAgent simulation
#    while(not a.terminated):
#        a.dumbAgent(w0)
    #once finish, print status
#    a.status()

    #Add score to an array
#    scoreList.append(a.score)
#    counter += 1

#print("Final results ")
#print("Score sim0 = "+str(s0_Score))
#print(scoreList)

