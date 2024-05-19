#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:49:58 2021
@author: jayesh

@teammate: Yoseph Kebede
"""

import numpy as np
import copy
import math
import time
import ast
import cv2
#import pygame
import matplotlib.pyplot as plt
import os
from queue import PriorityQueue
from actsetros1 import actionSet

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
xmax=1000                   #Width of the map
ymax=1000                    #Height of the map

#Child expansion variables
threshold=0.5                                   #Minimum difference between expanded nodes 
visited=[]                                      #List storing visited nodes
visited_nodes = np.zeros((2002,2002,25))          #Matrix storing visited nodes approximated with respect to threshold
act=actionSet()                                 #Instance of the actionSet class used to perform the child expansion actions

#Cost storing variables
cost2come = np.full((2002,2002,25),np.inf)        #Matrix storing cost from start to expanded nodes initialized to infinity
cost2goal = np.full((2002,2002,25),np.inf)        #Matrix storing cost from expanded nodes to goal initialized to infinity
totCost = np.full((2002,2002,25),np.inf)          #Matrix storing sum of cost to come and cost to goal initialized to infinity

#Backtracking variables
path_track={}               #Dictionary storing child nodes to a parent key

#Visualization variables
im_count=0
#pygame.init()               #Initializing Pygame
display_width = 1000         #Frame width
display_height = 1000        #Frame height
# gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
plt.ion()
fig, ax = plt.subplots()
#fig = plt.figure(num=1, figsize=(display_width, display_height), facecolor = 'black')
fig.suptitle("A* Animation")
# pygame.display.set_caption('A* Animation')
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
    print('checking goal')
    goal_thresh= 10
    if ((start[0]-goal[0]) ** 2 + (start[1]-goal[1])**2) <= (goal_thresh**2):
        return True
    else:
        return False
    
def round_15(child_ang):
        new_ang = int((round(child_ang/15)*15)//15)
        if new_ang==24:
            new_ang=0
        return new_ang
    
#Creating / Updating total cost of expanded nodes  
def cost_update(child,par,cost):
    child_ang=int((round(child[2]/15)*15)//15)
    par_ang=int((round(par[1][2]/15)*15)//15)
    #print('cost calc')
    x= child[0]; y = child[1]; z=int(child_ang)
    a = par[1][0]; b = par[1][1]; c = int(par_ang)
    #print('child par angle',child_ang,par_ang)
    if ((str([x,y]) not in riglist) and (x>0 and x<xmax) and (y>0 and y<ymax) and (child is not None)):
        if visited_nodes[2*x][2*y][z]==1:   
            print('visited')
            cost2come[2*x][2*y][z]= cost + cost2come[2*a][2*b][c]
            totCost1 = cost2come[2*x][2*y][z] + cost2goal[2*x][2*y][z]
            
            if totCost1 < totCost[2*x][2*y][z]:
               totCost[2*x][2*y][z] = totCost1
               child=[2*x,2*y,z]
               if str([2*a,2*b,c]) in path_track:
                   path_track[str([2*a,2*b,c])].append(child) 
               else:
                   path_track[str([2*a,2*b,c])]=[]
                   path_track[str([2*a,2*b,c])].append(child) 
                                             
        else:
            #print('not visited')
            visited_nodes[2*x][2*y][z]=1
            cost2come[2*x][2*y][z]=cost+cost2come[2*a][2*b][c]     #Calculating the new cost
            cost2goal[2*x][2*y][z]=c2gCalc([x,y],[g[0],g[1]])
            totCost[2*x][2*y][z]=cost2come[2*x][2*y][z]+cost2goal[2*x][2*y][z]
            #print(child,'q')
            q.put([totCost[2*x][2*y][z], child])                   #Updating the priority queue
            child=[2*x,2*y,z]
            #path_track[str([2*a,2*b,c])] = {}
            if str([2*a,2*b,c]) in path_track:
                path_track[str([2*a,2*b,c])].append(child)
            else:
                path_track[str([2*a,2*b,c])]=[]
                path_track[str([2*a,2*b,c])].append(child)
            #line.set_data(child[0]/2,1000-child[1]/2)
            #ax.plot([a, x], [b, y], color="blue")
            plt.scatter(child[0]/2,1000-child[1]/2, color="blue")
            # plt.draw()
            # plt.grid()
            # plt.set_aspect('equal')
            # plt.xlim(0,1)
            # plt.ylim(0,1)
            # plt.pause(0.05)
            # plt.show()
            # fig.matshow([child[0]/2,1000-child[1]/2], fignum=1, cmap= 'w')
            # plt.show()
            # pygame.event.get()     
            # pygame.display.flip()
            # pygame.draw.rect(gameDisplay, white, [child[0]/2,1000-child[1]/2,1,1])
            #pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{im_count}.png")
            #pygame.time.wait(5)
            #im_count+=1

    else:
        print('Obstacle')
        
def main(rpm1,rpm2):
    l=0
    while not q.empty(): #and l!=1:                                        #Process when queue is not empty
        
        a=q.get()                                               #Varibale to store the cost and node position
        #print('parent',a[1])
        x_n= a[1][0]; y_n = a[1][1]; z_n=(round(a[1][2]/15)*15)//15
        
        x_g= g[0]; y_g = g[1]; z_g = int(round(g[2]/15)*15)//15               #g[2]=30 for this project
        
        #Checking if goal is reached or not
        if goalReachCheck([x_n,y_n],[x_g, y_g]):
            print('goal',x_n,y_n,g)
            i=[x_g*2,y_g*2,z_g]
            visited.append([x_g,y_g])
            path_track[str([2*x_n,2*y_n,z_n])]=[]
            path_track[str([2*x_n,2*y_n,z_n])].append(i)
            print('goal reached')
            break
        
        l+=1
        print(l)
        #Getting the child nodes after moving in different positions with step size of 1 unit
        child1,cost1 = act.Action(a[1],0,rpm1)
        #print(child1)
        #print('cost1',cost1)
        cost_update(child1, a, cost1)
        child2,cost2 = act.Action(a[1],rpm1,0)
        #print('cost2',cost2,child2)
        cost_update(child2, a, cost2)
        child3,cost3= act.Action(a[1],rpm1,rpm1)
        cost_update(child3, a, cost3)
        child4,cost4 = act.Action(a[1],0,rpm2)
        cost_update(child4, a, cost4)
        child5,cost5 = act.Action(a[1],rpm2,0)
        cost_update(child5, a, cost5)
        child6,cost6= act.Action(a[1],rpm2,rpm2)
        cost_update(child6, a, cost6)
        child7,cost7 = act.Action(a[1],rpm1,rpm2)
        cost_update(child7, a, cost7)
        child8,cost8 = act.Action(a[1],rpm2,rpm1)
        cost_update(child8, a, cost8)
        #print(cost1,cost2,cost3,cost4,cost5,cost6,cost7,cost8)

def backtracking (start, goal):         #Backtracking to find the paths traversed from the initial state to the final state
    val = goal
    path_track_list=[]
    path_track_list.append(val)
    try:
        while val!=start:
            for key, values in path_track.items():
                while val in values:
                    key= ast.literal_eval(key)                  #converting strings of lists to pure lists
                    val = key
                    path_track_list.append(val)
    except KeyError:
        print('value not found')
        
    return path_track_list

def visualization():                            #Creating an animation using pygame 
    # pygame.event.get()    
    # gameDisplay.fill(black)

    #Setting the obstacle space in the animation
    for path in oblist1:
        x = int(path[0])
        y = abs(1000-int(path[1]))
        plt.scatter(x, y, color="blue")
        # plt.draw()
        # plt.grid()
        # plt.set_aspect('equal')
        # plt.xlim(0,1)
        # plt.ylim(0,1)
        # plt.pause(0.05)
        # ax.show()
        # fig.matshow([x,y], fignum=1, cmap= 'r')
        # plt.show()
        #pygame.display.flip()
        # pygame.draw.rect(gameDisplay, yellow, [x,y,1,1])
        #pygame.time.wait(0)
    
##################################################### Code execution starts here #######################################################
if __name__ == "__main__":

    oblist1, riglist=act.getobstaclespace()                         #Retrieve obstacle and clearance information
    visualization()
    while True:
        x1=int(input('Enter x coordinate of start node: '))
        y1=int(input('Enter y coordinate of start node: '))
        theta=int(input('Enter degree of start node: '))           #theta for this project is 30
        s = [x1,y1,theta]                                              #Start Position
        rpm1=int(input('Enter rpm of left wheel: '))
        rpm2=int(input('Enter rpm of right wheel: '))
        x2=int(input('Enter x coordinate of goal node: '))
        y2=int(input('Enter y coordinate of goal node: '))
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
    z=int(round(s[2]/15)*15)//15
    #print(z)
    visited_nodes[2*x1][2*y1][z]=1
    #print('visited')
    #Initializing the cost to come of start point to zero
    cost2come[2*x1][2*y1][z] = 0
    
    #Initializing the cost2goal for start node
    cost2goal[2*x1][2*y1][z] =  c2gCalc(start,goal)
    
    #Updating the total heurisitc for start node
    totCost[2*x1][2*y1][z] = cost2come[2*x1][2*y1][z] + cost2goal[2*x1][2*y1][z]
    #print(totCost[2*x1][2*y1][z])
    #Initializing the queue with a Total cost and the start node
    q.put([totCost[2*x1][2*y1][z], s])              
    '''
    #Initializing Parent Child dictionary
    for i in range(0, xmax+1):
        for j in range(0, ymax+1):
            for k in range(0,25):
                #print('stuck')
                path_track[str([2*i, 2*j, k])] = []
    '''
    start_time = time.time()            #Program start time
    print('before main')
    main(rpm1,rpm2)                              #Executing search
    
    #Time to reach goal state
    print('time to reach goal',time.time()-start_time)
    
    #Converting start and goal node with threshold of 0.5 units
    s=[2*x1,2*y1,int(s[2]/15)]
    g=[2*x2,2*y2,int(g[2]/15)]
    print(g)

    print('path track',path_track)
    #Performing backtracking to obtain list for optimal path
    path_track_list = backtracking(s, g)
    
    path1=[]
    #print(path)
    
    #print('path track',path_track_list)
    for path in path_track_list:
        #pygame.event.get()
        x = path[0]/2
        y = abs(1000-path[1]/2)
        path1.append((x,y))
        #pygame.display.flip()
        #print('displaying')
        print(x,y)
        #pygame.draw.rect(gameDisplay, (255,5,5), [x,y,10,10])
        #pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{im_count}.png")         #Saving the images to create a video                                                                                         #uncomment if not required
        #im_count+=1
       #pygame.time.wait(5000)
    #while True: 
    for i in range(len(path1)):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        plt.scatter(path1, color="blue")
        #plt.draw()
        
    plt.grid()
    plt.set_aspect('equal')
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.title('A* Animation')
    plt.show()
    plt.iof()
    plt.close()
        # fig.matshow(path1, fignum=1, cmap= 'r')
        # plt.show()     
        # pygame.display.flip()
        # pygame.draw.lines(gameDisplay, (255,5,5), False, path1, 2)
        # pygame.time.wait(500)
        # pygame.display.update()

    #Terminate Pygame
    #pygame.quit()

    #Print the total time taken to reach goal state and backtrack
    print("total time:")
    print(time.time()-start_time)

############################################# Code Execution ends here #############################################################