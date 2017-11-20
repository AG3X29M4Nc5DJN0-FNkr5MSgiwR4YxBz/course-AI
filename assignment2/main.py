from wumpusWorld import *
from agent import *
from knowledgeAgent import *

#Create a world and an agent
#Simulation 0

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

w0.printRoom()
#Create agent
print("Creating Agent")
a0 = agent(0,0)
a0.updatePercept(w0)
print(a0.percept)
print(a0.position)

#Create KB
print("Creating kb")
wKB0 = wumpusKB(w0)
print(a0.percept)
print(a0.position)


wKB0.addPercept(a0.percept,a0.position[0],a0.position[1])

#Agent walks to 1,0

a0.performAction("move_forward",w0)

print(a0.percept)
print(a0.position)

wKB0.addPercept(a0.percept,a0.position[0],a0.position[1])

print(wKB0.kb.clauses)

print("0,0 safe : " +str(wKB0.safe(0,0)))
print("0,1 safe : " +str(wKB0.safe(0,1)))
print("1,0 safe : " +str(wKB0.safe(1,0)))
print("1.1 safe : " +str(wKB0.safe(1,1)))
print("2,0 safe : " +str(wKB0.safe(2,0)))
print("2,1 safe : " +str(wKB0.safe(2,1)))

#Walc to 0,0
a0.performAction("turn_left",w0)

a0.performAction("turn_left",w0)

a0.performAction("move_forward",w0)
print(a0.percept)
print(a0.position)

wKB0.addPercept(a0.percept,a0.position[0],a0.position[1])


#Walk to 0,1

a0.performAction("turn_right",w0)
a0.performAction("move_forward",w0)
print(a0.percept)
print(a0.position)

wKB0.addPercept(a0.percept,a0.position[0],a0.position[1])

#check 1,1 should return true

print("1,1 safe : " +str(wKB0.safe(1,1)))
print("0,2 safe : " +str(wKB0.safe(0,2)))

#Walk to 1,1

a0.performAction("turn_right",w0)
a0.performAction("move_forward",w0)
print(a0.percept)
print(a0.position)

wKB0.addPercept(a0.percept,a0.position[0],a0.position[1])
print("0,0 safe : " +str(wKB0.safe(0,0)))
print("0,1 safe : " +str(wKB0.safe(0,1)))
print("1,0 safe : " +str(wKB0.safe(1,0)))
print("1.1 safe : " +str(wKB0.safe(1,1)))
print("2,0 safe : " +str(wKB0.safe(2,0)))
print("2,1 safe : " +str(wKB0.safe(2,1)))






