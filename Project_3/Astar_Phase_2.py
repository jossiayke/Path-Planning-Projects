#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 08:20:17 2021
@author: jayesh
@teammate: Yoseph Kebede
"""

import numpy as np
import copy
import math
import time
import ast
import cv2
import pygame
import os
from queue import PriorityQueue
from actSetStar import actionSet

#Start and Goal Nodes
s = []                      #List storing user input start node
g = []                      #List storing user input goal node

#Obstacle variables
oblist1=[]                  #List to store the obstacle coordinates for final animation
riglist=set([])             #List to store obstacle with clearance
radius=10                   #Radius of Mobile Robot
clearance=5                 #Clearance distance from/around obstacles
dist=radius+clearance       #Total clearance between point robot and obstacle

#Enironment variables
xmax=400                    #Width of the map
ymax=300                    #Height of the map

#Child expansion variables
threshold=0.5                                   #Minimum difference between expanded nodes 
visited=[]                                      #List storing visited nodes
visited_nodes = np.zeros((801,601,13))          #Matrix storing visited nodes approximated with respect to threshold
act=actionSet()                                 #Instance of the actionSet class used to perform the child expansion actions

#Cost storing variables
cost2come = np.full((801,601,13),np.inf)        #Matrix storing cost from start to expanded nodes initialized to infinity
cost2goal = np.full((801,601,13),np.inf)        #Matrix storing cost from expanded nodes to goal initialized to infinity
totCost = np.full((801,601,13),np.inf)          #Matrix storing sum of cost to come and cost to goal initialized to infinity

#Backtracking variables
path_track={}               #Dictionary storing child nodes to a parent key

#Visualization variables
im_count=0
pygame.init()               #Initializing Pygame
display_width = 400         #Frame width
display_height = 300        #Frame height
gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.SCALED)
pygame.display.set_caption('A* Animation')
black = (0,0,0)         #Color represnting the background of image
white = (0,255,255)     #Color respresenting the visited nodes
yellow=(255,255,0)      #Color representing the obstacles

#Temporary Queue variables
q = PriorityQueue()         #Setting a priority queue

#Nodes cost calculation
def c2gCalc(start,goal):
    #euclidean distance of goal
    dist=math.sqrt((start[0]-goal[0]) ** 2 + (start[1]-goal[1])**2)
    return dist

#Confirming expanded node has reached goal space
def goalReachCheck(start,goal):
    goal_thresh= 1.5
    if ((start[0]-goal[0]) ** 2 + (start[1]-goal[1])**2) <= (goal_thresh**2):
        return True
    else:
        return False

#Creating / Updating total cost of expanded nodes  
def cost_update(child,par,cost):
    x= child[0]; y = child[1]; z=int(child[2]/30)
    a = par[1][0]; b = par[1][1]; c = int(par[1][2]/30)

    if ((str([x,y]) not in riglist) and (x>0 and x<xmax) and (y>0 and y<ymax) and (child is not None)):
        if visited_nodes[2*x][2*y][z]==1:   
            cost2come[2*x][2*y][z]= cost + cost2come[2*a][2*b][c]
            totCost1 = cost2come[2*x][2*y][z] + cost2goal[2*x][2*y][z]
            
            if totCost1 < totCost[2*x][2*y][z]:
               totCost[2*x][2*y][z] = totCost1
               child=[2*x,2*y,z]
               path_track[str([2*a,2*b,c])].append(child)  
                              
               
        else:
            visited_nodes[2*x][2*y][z]=1
            cost2come[2*x][2*y][z]=cost+cost2come[2*a][2*b][c]     #Calculating the new cost
            cost2goal[2*x][2*y][z]=c2gCalc([x,y],[g[0],g[1]])
            totCost[2*x][2*y][z]=cost2come[2*x][2*y][z]+cost2goal[2*x][2*y][z]
            q.put([totCost[2*x][2*y][z], child])                   #Updating the priority queue
            child=[2*x,2*y,z]
            path_track[str([2*a,2*b,c])].append(child)
    
            pygame.display.flip()
            pygame.draw.rect(gameDisplay, white, [x/2,300-y/2,1,1])
            pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{im_count}.png")
            im_count+=1
def main():
    l=0
    while not q.empty():                                        #Process when queue is not empty
        
        a=q.get()                                               #Varibale to store the cost and node position
        x_n= a[1][0]; y_n = a[1][1]; z_n = int(a[1][2]/30)
        x_g= g[0]; y_g = g[1]; z_g = int(g[2]/30)               #g[2]=30 for this project
        
        #Checking if goal is reached or not
        if goalReachCheck([x_n,y_n],[x_g, y_g]):
            print('goal',x_n,y_n,g)
            i=[x_g*2,y_g*2,z_g]
            visited.append([x_g,y_g])
            path_track[str([2*x_n,2*y_n,z_n])].append(i)
            print('goal reached')
            break

        l+=1
        
        #Getting the child nodes after moving in different positions with step size of 1 unit
        childz = act.ActionZero(a[1],3)
        cost_update(childz, a, 1)
        childp30 = act.ActionP30(a[1],30,3)
        cost_update(childp30, a, 1)
        childp60= act.ActionP60(a[1],30,3)
        cost_update(childp60, a, 1)
        childn30 = act.ActionN30(a[1],30,3)
        cost_update(childn30, a, 1)
        childn60 = act.ActionN60(a[1],30,3)
        cost_update(childn60, a, 1)

def backtracking (start, goal):         #Backtracking to find the paths traversed from the initial state to the final state
    val = goal
    path_track_list=[]
    path_track_list.append(val)

    while val!=start:
        for key, values in path_track.items():
            while val in values:
                key= ast.literal_eval(key)                  #converting strings of lists to pure lists
                val = key
                path_track_list.append(val)

    return path_track_list

def visualization():                            #Creating an animation using pygame    
    gameDisplay.fill(black)

    #Setting the obstacle space in the animation
    for path in oblist1:
        x = int(path[0])
        y = abs(300-int(path[1]))
        pygame.display.flip()
        pygame.draw.rect(gameDisplay, yellow, [x,y,1,1])
        #pygame.time.wait(0)
    
##################################################### Code execution starts here #######################################################
if __name__ == "__main__":

    oblist1, riglist=act.getobstaclespace()                         #Retrieve obstacle and clearance information
    visualization()
    while True:
        x1=int(input('Enter x coordinate of start node: '))
        y1=int(input('Enter y coordinate of start node: '))
        #theta=int(input('Enter degree of start node: '))           *theta for this project is 30
        s = [x1,y1,30]                                              #Start Position
        x2=int(input('Enter x coordinate of goal node: '))
        y2=int(input('Enter y coordinate of goal node: '))
        #gtheta=int(input('Enter degree of goal node: '))           *gtheta for this project is 30
        g = [x2,y2,30]                                              #Goal Position

        start= [x1, y1]
        goal = [x2, y2]

        if goalReachCheck(start,goal):                              #Checking if goal node is the same as the start node
            print('start node equal to/within threshold of goal node. Re enter your points again')
            continue

        elif str(start) in riglist:                                  #Checking if start node is in the obstaclespace plus clearance
            print('Start node in obstacle space. Re enter the points again')
            continue
        elif str(goal) in riglist:                                   #Checking if goal node is in the obstaclespace plus clearance
            print('Goal node in obstacle space. Re enter the points again')
            continue

        elif (x1 <0 or x1> xmax) or (y1<0 or y1 > ymax):    #Checking if start node is within the grid(400x300)
            print('start node is outside environment. Re enter the points again')
            continue 

        elif (x2 <0 or x2> xmax) or (y2<0 or y2 > ymax):        #Checking if goal node is within the grid(400X300)
            print('Goal node is outside Environment. Re enter the points again')
            continue

        else:
            break

    print(s)
    print(g)
    visited.append(start)
    visited_nodes[2*x1][2*y1][int(s[2]/30)]=1
    
    #Initializing the cost to come of start point to zero
    cost2come[2*x1][2*y1][int(s[2]/30)] = 0

    #Initializing the cost2goal for start node
    cost2goal[2*x1][2*y1][int(s[2]/30)] =  c2gCalc(start,goal)

    #Updating the total heurisitc for start node
    totCost[2*x1][2*y1][int(s[2]/30)] = cost2come[2*x1][2*y1][int(s[2]/30)] + cost2goal[2*x1][2*y1][int(s[2]/30)]
    
    #Initializing the queue with a Total cost and the start node
    q.put([totCost[2*x1][2*y1][int(s[2]/30)], s])              
    
    #Initializing Parent Child dictionary
    for i in range(0, xmax+1):
        for j in range(0, ymax+1):
            for k in range(0,13):
                path_track[str([2*i, 2*j, k])] = []
             
    start_time = time.time()            #Program start time
    main()                              #Executing search
    
    #Time to reach goal state
    print('time to reach goal',time.time()-start_time)
    
    #Converting start and goal node with threshold of 0.5 units
    s=[2*x1,2*y1,int(s[2]/30)]
    g=[2*x2,2*y2,int(g[2]/30)]
    print(g)

    #Performing backtracking to obtain list for optimal path
    path_track_list = backtracking(s, g)
    
    path=[path_track_list[0],path_track_list[1]]
    print(path)
    for path in path_track_list:
        x = path[0]/2
        y = abs(300-path[1]/2)
        pygame.display.flip()
        pygame.draw.rect(gameDisplay, (255,5,5), [x,y,1,1])
        pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{im_count}.png")         #Saving the images to create a video                                                                                         #uncomment if not required
        im_count+=1
        pygame.time.wait(50)
    
    #Terminate Pygame
    pygame.quit()

    #Print the total time taken to reach goal state and backtrack
    print("total time:")
    print(time.time()-start_time)

############################################# Code Execution ends here #############################################################
