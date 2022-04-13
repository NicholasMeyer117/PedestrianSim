#Nicholas Meyer
#Pedestrian Simulation
#Animation 1
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
def getCostAtPos(xPos, yPos, goal, obsCoords, wallCoords, ballCoords, ballNum):
    #Goal Cost
    goalCost = np.sqrt(np.power(xPos - goal[0], 2) + np.power(yPos - goal[1], 2))

    #Wall Penalty
    wallPenalty = 0
    wallRadius = 5
    for wall in wallCoords:
        wallDist = np.sqrt(np.power(xPos - wall[0], 2) + np.power(yPos - wall[1], 2))
        wallPenalty = wallPenalty + findFieldPenalty(wallDist, wallRadius)

    #Cylinder Penalty
    obsRadius = 14
    obsDist = np.sqrt(np.power(xPos - obsCoords[0], 2) + np.power(yPos - obsCoords[1], 2))
    obsPenalty = findFieldPenalty(obsDist, obsRadius)

    #Total field penalty
    fieldPenalty = wallPenalty + (obsPenalty * 2)

    #Ball Penalty
    ballPenalty = 0
    for i in range(len(ballCoords)):
        if i != ballNum:
            ballRadius = 5
            ballDist = np.sqrt(np.power(xPos - ballCoords[i][0], 2) + np.power(yPos - ballCoords[i][1], 2))
            ballPenalty = ballPenalty + findFieldPenalty(ballDist, ballRadius)

    # Goal Cost + All penalties
    cost = goalCost + (fieldPenalty * 5) + (ballPenalty * 5)

    return cost

#Sets up canvas
canvas(width=900,height=400,background=color.black)
base = box(pos=vector(0,0,0), length=200, height=100, width=1, color = color.blue)

#Creates 3D objects
ballList = []
for i in range(5):
    ballList.append(sphere(pos = vector(-50 + random.uniform(0, 5), 20 - (i * 12), 0.5), radius = 2, color = color.green, retain = 200))
for i in range(5):
    ballList.append(sphere(pos = vector(-40 + random.uniform(0, 5), -20 + (i * 12), 0.5), radius = 2, color = color.green, retain = 200))
for i in range(5):
    ballList.append(sphere(pos = vector(-30 + random.uniform(0, 5), 20 - (i * 12), 0.5), radius = 2, color = color.green, retain = 200))

wall1 = box(pos=vector(40, 25, 10), length=5.0, height=40, width=2, color = color.red)
wall2 = box(pos=vector(40, -25, 10), length=5.0, height=40, width=2, color = color.red)
obs = cylinder(pos=vector(0, 0, 0), axis=vector(0, 0, 20), radius=7, color = color.red)

ballCoordsList = []
for ball in ballList:
    ballCoordsList.append([ball.pos.x+100, ball.pos.y + 50])

goal = [190, 50]
obsCoords = [100, 50]
wall1Coords = []
wall2Coords = []
for i in range(45):
    wall1Coords.append([140, (i * 1)])
for i in range(45):
    wall2Coords.append([140, 100 - (i * 1)])

wallCoords = wall1Coords + wall2Coords

scene.camera.pos = vector(0,-20,20)

#Loops until program is stopped
#Iterates through each ball and finds its cost, then finds the gradient, and moves the ball
while True:
    rate(5)
    ballNum = 0
    for ball in ballList:
        cost = getCostAtPos(ballCoordsList[ballNum][0], ballCoordsList[ballNum][1], goal, obsCoords, wallCoords, ballCoordsList, ballNum)
        costX = getCostAtPos(ballCoordsList[ballNum][0] + 0.0001, ballCoordsList[ballNum][1] , goal, obsCoords, wallCoords, ballCoordsList, ballNum)
        costY = getCostAtPos(ballCoordsList[ballNum][0], ballCoordsList[ballNum][1]+0.0001, goal, obsCoords, wallCoords, ballCoordsList, ballNum)

        # Find gradient and divide by the absolute value of itself to create a smooth single speed
        gradient = [(cost - costX)/0.00003, (cost - costY)/0.00003]
        gradient = [gradient[0]/abs(gradient[0]), gradient[1]/abs(gradient[1])]

        ball.pos = ball.pos + vector(gradient[0]/3, gradient[1]/3, 0)
        ballCoordsList[ballNum][0] = ballCoordsList[ballNum][0] + gradient[0]/3
        ballCoordsList[ballNum][1] = ballCoordsList[ballNum][1] + gradient[1]/3
        ballNum = ballNum + 1


