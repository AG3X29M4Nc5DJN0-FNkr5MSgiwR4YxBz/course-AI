from wumpusWorld import *
from agent import *
from knowledgeAgent import *

w0 = wumpusWorld()
#Set the world
for i in range(0,4):
    for j in range(0,4):
        w0.r[i][j] = room()
w0.r[2][0].pit = True
w0.r[0][2].wumpus = True
w0.r[1][2].gold = True
w0.r[2][2].pit = True
w0.r[3][3].pit = True
w0.r[0][0].agent = True

#Create agent
print("Creating Agent")
a0 = agent(0,0,w0)

w0.printRoom()
while(not a0.terminated):
    a0.dumbAgent(w0)
    w0.printRoom()
    a0.status()

s0_Score = a0.score

counter = 0
scoreList = []
while(counter < 10000):
    #Create a new world
    w = wumpusWorld()
    #create a new agent
    a = agent(0,0,w)
    #Do the testDumbAgent simulation
    while(not a.terminated):
        a.dumbAgent(w0)
    #once finish, print status
    a.status()

    #Add score to an array
    scoreList.append(a.score)
    counter += 1

print("Final results ")
print("Score sim0 = "+str(s0_Score))
print(scoreList)

