from wumpusWorld import *
from agent import *
from knowledgeAgent import *

w0 = wumpusWorld()


#Set the world

for i in range(0,4):
    for j in range(0,4):
        w0.r[i][j] = room()

#world#0 - original simulation

w0.r[2][0].pit = True
w0.r[0][2].wumpus = True
w0.r[1][2].gold = True
w0.r[2][2].pit = True
w0.r[3][3].pit = True
w0.r[0][0].agent = True

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

#World #4. bug : sometimes when moving agents world didnt remove older one
#w0.r[3][1].wumpus = True
#w0.r[2][3].gold = True
#w0.r[2][2].pit = True


#[] [] [P] [G]
#[WA] [] [P] []
#[] [P] [] []
#[] [] [] [P]

#World #5, bug : should've known there was a wumpus at 0,2 since we didnt smell it at 1,0
#Fix : uncommented the rules saying a wumpus must be smelly at every adjacent squares
#TODO this fix bugged other cases, maybe we can find a better rule?
#w0.r[1][1].pit = True
#w0.r[0][2].wumpus = True
#w0.r[3][0].pit = True
#w0.r[2][2].pit= True
#w0.r[2][3].pit = True
#w0.r[3][3].gold = True

#[] [] [P] [] 
#[] [P] [] [] 
#[] [WA] [] [G] 
#[] [P] [P] [] 

#World #6, bug : thing 1,1 is safe
#w0.r[1][0].pit = True
#w0.r[1][1].wumpus = True
#w0.r[3][1].gold = True


#Test w0

a = agent(0,0,w0)
while(not a.terminated):
    w0.printRoom()
    a.status()
    a.smartAgent(w0)

a.status()
w0.printRoom()

#scoreTotal = 0
#for i in range(10000):
#    print("[+] Simulation #"+str(i))
#    w = wumpusWorld()
#    a = agent(0, 0, w)
#    while(not a.terminated):
#        a.astar_Agent(w)
#    a.status()
#    print("")
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

