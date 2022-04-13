#Nicholas Meyer
#Pedestrian Simulation
#Animation 2
from vpython import *
import numpy as np
import random

# Field penalty function
# Uses distances and radius of obstacles to calculate and return field penalty
def findFieldPenalty(d,R):
    if 0 < d <= R:
        return np.log(np.divide(R,d))
    else:
       return 0

# Gets the cost for a sphere at its current position
def getCostAtPos(xPos, yPos, goal, wallCoords, ballCoords, ballNum):

    # Goal Cost
    goalCost = np.sqrt(np.power(xPos - goal[0], 2) + np.power(yPos - goal[1], 2))

    #Penalty from obstacles
    wallPenalty = 0
    wallRadius = 5
    for wall in wallCoords:
        wallDist = np.sqrt(np.power(xPos - wall[0], 2) + np.power(yPos - wall[1], 2))
        wallPenalty = wallPenalty + findFieldPenalty(wallDist, wallRadius)

    fieldPenalty = wallPenalty

    # Penalty from other balls
    ballPenalty = 0
    for i in range(len(ballCoords)):
        if i != ballNum:
            ballRadius = 5
            ballDist = np.sqrt(np.power(xPos - ballCoords[i][0], 2) + np.power(yPos - ballCoords[i][1], 2))
            ballPenalty = ballPenalty + findFieldPenalty(ballDist, ballRadius)


    #Goal Cost + All penalties
    cost = goalCost + (fieldPenalty * 5) + (ballPenalty * 5)

    return cost

#Sets up Canvas
canvas(width=900,height=400,background=color.black)
base = box(pos=vector(0,0,0), length=200, height=200, width=1, color = color.blue)
scene.camera.pos = vector(0,-5,-50)

#Creates 3D objects
ballList = []
for i in range(5):
    ballList.append(sphere(pos = vector(-100 + random.uniform(0, 5) + (i * 10), 5, 0.5), radius = 2, color = color.green, retain = 200))
for i in range(5):
    ballList.append(sphere(pos = vector(-100 + random.uniform(0, 5) + (i * 10), -5, 0.5), radius = 2, color = color.green, retain = 200))
for i in range(5):
    ballList.append(sphere(pos = vector(7, 95 - (i * 10) + random.uniform(0, 5), 0.5), radius = 2, color = color.red, retain = 200))
for i in range(5):
    ballList.append(sphere(pos = vector(12, 100 - (i * 10) + random.uniform(0, 5), 0.5), radius = 2, color = color.red, retain = 200))

wall1 = box(pos=vector(20, 55, 10), length=2.5, height=85, width=10, color = color.red)
wall2 = box(pos=vector(0, 55, 10), length=2.5, height=85, width=10, color = color.red)
wall3 = box(pos=vector(-45, 10, 10), length=90, height=2.5, width=10, color = color.red)
wall4 = box(pos=vector(65, 10, 10), length=90, height=2.5, width=10, color = color.red)
wall5 = box(pos=vector(0, -10, 10), length=200, height=2.5, width=10, color = color.red)

ballCoordsList = []
for ball in ballList:
    ballCoordsList.append([ball.pos.x+100, ball.pos.y + 50])

goal = [190, 50]
wall1Coords = []
wall2Coords = []
wall3Coords = []
wall4Coords = []
wall5Coords = []
for i in range(70):
    wall1Coords.append([120, 200 - (i * 2)])
for i in range(72):
    wall2Coords.append([100, 200 - (i * 2)])
for i in range(50):
    wall3Coords.append([(i * 2), 60])
for i in range(40):
    wall4Coords.append([120 + (i * 2), 60])
for i in range(50):
    wall5Coords.append([(i * 4), 40])

wallCoords = wall1Coords + wall2Coords + wall3Coords + wall4Coords + wall5Coords

#Loops until program is stopped
#Iterates through each ball and finds its cost, then finds the gradient, and moves the ball
while True:
    rate(5)
    ballNum = 0
    for ball in ballList:
        #Find cost
        cost = getCostAtPos(ballCoordsList[ballNum][0], ballCoordsList[ballNum][1], goal, wallCoords, ballCoordsList, ballNum)
        costX = getCostAtPos(ballCoordsList[ballNum][0] + 0.0001, ballCoordsList[ballNum][1] , goal, wallCoords, ballCoordsList, ballNum)
        costY = getCostAtPos(ballCoordsList[ballNum][0], ballCoordsList[ballNum][1]+0.0001, goal, wallCoords, ballCoordsList, ballNum)

        # Find gradient and move ball
        gradient = [(cost - costX)/0.00003, (cost - costY)/0.00003]
        ball.pos = ball.pos + vector(gradient[0]/3, gradient[1]/3, 0)
        ballCoordsList[ballNum][0]= ballCoordsList[ballNum][0] + gradient[0]/3
        ballCoordsList[ballNum][1] = ballCoordsList[ballNum][1] + gradient[1]/3
        ballNum = ballNum + 1

