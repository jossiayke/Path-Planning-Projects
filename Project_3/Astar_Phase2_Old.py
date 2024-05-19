#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 08:20:17 2021
@author: jayesh
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


goal=[]
#g=[]
oblist1=[]       #List to store the obstacle coordinates for final animation
riglist=set([])
radius=10
clearance=5
dist=radius+clearance
xmax=10                    #Width of the map
ymax=10                    #Height of the map
threshold=0.5
visited=[]
cost2come = np.full((801,601,13),np.inf)
cost2goal = np.full((801,601,13),np.inf)
totCost = np.full((801,601,13),np.inf)
solvable=False
visited_nodes = np.zeros((801,601,13))
path_track={}               #Dictionary storing the parent nodes of the different child nodes to backtrack the path followed

im_count=0
pygame.init()

display_width = 400
display_height = 300

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.SCALED)
pygame.display.set_caption('Djikstra Animation')

black = (0,0,0)         #Color represnting the background of image
white = (255,255,255)     #Color respresenting the visited nodes
yellow=(255,255,0)      #Color representing the obstacles

l=0
q = PriorityQueue()         #Setting a priority queue
#distance = {}               #Dictionary to store the distance of a node from the previous node
#distancec2g={}

act=actionSet()

def cos2goal(start,goal):
    #euclidean distance of goal
    dist=math.sqrt((start[0]-goal[0]) ** 2 + (start[1]-goal[1])**2)
    return dist

def cos2come(curr_position,goal):
    #print('c2c')
    #print(curr_position[1],goal[1],curr_position[0],goal[0])
    manhattan_distance = abs(curr_position[1] - goal[1]) + abs(curr_position[0] - goal[0])
    return manhattan_distance

def goalReachCheck(start,goal):
    #Checking of euclidean distance <= 1.5**2
    #print('goal check')
    goal_thresh= 1.5
    #print(start[0],start[1],goal[0],goal[1])
    if ((start[0]-goal[0]) ** 2 + (start[1]-goal[1])**2) <= (goal_thresh**2):
        #print((start[0]-goal[0]) ** 2 + (start[1]-goal[1])**2,goal_thresh**2)
        return True
    else:
        return False
    
def cost_update(child,par,cost):
    #print('costupdate')
    #print(str([child[0],child[1]]))
    #if str([child[0],child[1]]) in riglist:
        #print('rigid')
    global im_count
    #Checking if the child nodes are visited or not, if they lie within the resolution specified and if present in the obstacle space
    if (str([child[0],child[1]]) not in riglist) and (child[0]>0 and child[0]<xmax) and (child[1]>0 and child[1]<ymax) and (child is not None):
        #print('visit check')
        #print(child[0])
        #print(child[1])
        #print(child[2]/30)
        
        #print(visited_nodes[2*child[0]][2*child[1]][int(child[2]/30)])
        if visited_nodes[2*child[0]][2*child[1]][int(child[2]/30)]==1:
            #print('visited')    
            cost2come[2*child[0]][2*child[1]][int(child[2]/30)]=cost+cost2come[2*par[1][0]][2*par[1][1]][int(par[1][2]/30)]
            totCost1 =cost2come[2*child[0]][2*child[1]][int(child[2]/30)]+cost2goal[2*child[0]][2*child[1]][int(child[2]/30)]
            if totCost1 < totCost[2*child[0]][2*child[1]][int(child[2]/30)]:
               totCost[2*child[0]][2*child[1]][int(child[2]/30)] = totCost1
               #print('par',par[1][0],par[1][1])
               #print('child',child[0],child[1])
               child=[2*child[0],2*child[1],int(child[2]/30)]
               path_track[str([2*par[1][0],2*par[1][1],int(par[1][2]/30)])].append(child)  
               
               
        else:
            #print('Adding')
            visited_nodes[child[0]*2][child[1]*2][int(child[2]/30)]=1
            cost2come[2*child[0]][2*child[1]][int(child[2]/30)]=cost+cost2come[2*par[1][0]][2*par[1][1]][int(par[1][2]/30)]     #Calculating the new cost
            cost2goal[2*child[0]][2*child[1]][int(child[2]/30)]=cos2goal([child[0],child[1]],goal)
            totCost[2*child[0]][2*child[1]][int(child[2]/30)]=cost2come[2*child[0]][2*child[1]][int(child[2]/30)]+cost2goal[2*child[0]][2*child[1]][int(child[2]/30)]
            q.put([totCost[2*child[0]][2*child[1]][int(child[2]/30)], child])              #Updating the priority queue
            #print('par',2*par[1][0],2*par[1][1],par[1][2]/30)
            #print('child',2*child[0],2*child[1],child[2]/30)
            #path_track[str([2*par[1][0],2*par[1][1],int(par[1][2]/30)])].append([2*child[0]][2*child[1]][int(child[2]/30)])
            child=[2*child[0],2*child[1],int(child[2]/30)]
            path_track[str([2*par[1][0],2*par[1][1],int(par[1][2]/30)])].append(child)
            pygame.display.flip()
            pygame.draw.rect(gameDisplay, white, [child[0]/2,300-child[1]/2,1,1])
            
            pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{im_count}.png")
            im_count+=1
            #pygame.time.wait(2)
            
                
def main():
    l=0
    while not q.empty():  #Process when queue is not empty
        #print('loop',l)
        a=q.get()         #Varibale to store the cost and node position
        #print('queue',a[0],a[1],len(a))
        #print(g[0],g[1],a[1][0],a[1][1])
        
        #Inititalizing the dictionary to store information related to the parent node
        
        
        #Checking if goal is reached or not
        if goalReachCheck([a[1][0],a[1][1]],[g[0],g[1]]):
            
            print('goal',a[1][0],a[1][1],g)
            g[2]=30
            i=[g[0]*2,g[1]*2,int(g[2]/30)]
            visited.append([g[0],g[1]])
            #path_track[str([a[1][0],a[1][1]])] = []
            path_track[str([2*a[1][0],2*a[1][1],int(a[1][2]/30)])].append(i)
            print('goal reached')
            break

        l+=1
        
        #Getting the child nodes after moving in different positions
        childz = act.ActionZero(a[1],3)
        #print(a[1][0],a[1][1],childz[0],childz[1])

        cost_update(childz, a, 1)
        childp30 = act.ActionP30(a[1],30,3)

        cost_update(childp30, a, 1)
        childp60= act.ActionP60(a[1],30,3)

        cost_update(childp60, a, 1)
        childn30 = act.ActionN30(a[1],30,3)

        cost_update(childn30, a, 1)
        childn60 = act.ActionN30(a[1],30,3)  #I had a typo here

        cost_update(childn60, a, 1)


def backtracking (start, goal):
    #Backtracking to find the paths traversed from the initial state to the final state
    final_state = goal
    val = goal
    #print('val',val)
    goal = start
    path_track_list=[]
    #print('Parent track',path_track)
    #print('start',start)
    path_track_list.append(final_state)
    while val!=goal:
        #print('val',val)
        for key, values in path_track.items():
            #print('key',key,values,'val',val)
            
            while val in values:
                #print('val',val)
                #print('appending')
                key= ast.literal_eval(key) #converting strings of lists to pure lists
                val = key
                path_track_list.append(val)

    return path_track_list

def visualization():
    #Creating an animation using pygame
    
    i=0
    #surf = pygame.surfarray.make_surface(img)

    clock = pygame.time.Clock()
    done = False
    

    gameDisplay.fill(black)

        #Setting the obstacle space in the animation
    for path in oblist1:
        x = int(path[0])
        y = abs(300-int(path[1]))
        pygame.display.flip()
        pygame.draw.rect(gameDisplay, yellow, [x,y,1,1])
                #pygame.time.wait(0)

#### Code execution starts here #####
if __name__ == "__main__":
    
    oblist1, riglist=act.getobstaclespace()
    visualization()
    while True:
        x1=int(input('Enter x coordinate of start node: '))
        y1=int(input('Enter y coordinate of start node: '))
        theta=int(input('Enter degree of start node: '))
        s = [x1,y1,theta]
        x2=int(input('Enter x coordinate of goal node: '))
        y2=int(input('Enter y coordinate of goal node: '))
        gtheta=int(input('Enter degree of goal node: '))
        g = [x2,y2,gtheta]                 #Goal Position Test Case2

        start=[]
        startx=s[0]
        starty=s[1]
        start=[startx,starty]

        goalx=g[0]
        goaly=g[1]
        goal=[goalx,goaly]

        if goalReachCheck(start,goal): #Checking if goal node is the same as the start node
            print('start node equal to/within threshold of goal node. Re enter your points again')
            continue

        elif str(start) in riglist or str(goal) in riglist: #checking if the goal or start node is in the obstaclespace including radius and clearance
            print('Starting or goal node in obstacle space. Re enter the points again')
            continue

        elif (start[0] <0 or start[0]> xmax) or (start[1]<0 or start[1] > ymax) or (goal[0] <0 or goal[0]> xmax) or (goal[1]<0 or goal[1] > ymax): #Checking if the start and goal node is within the grid(400x300)
            print('start/goal < 0 or greater than grid size. Re enter the points again')

        else:
            break

    print(s)
    print(g)
    visited.append(start)
    visited_nodes[2*s[0]][2*s[1]][int(s[2]/30)]=1
    #cost2come[0][0][0]=1
    #print(cost2come[0][0][0],s[1],s[2],s[0])
    #Initializing the cost to come of start point to zero
    cost2come[2*s[0]][2*s[1]][int(s[2]/30)] = 0

    #Initializing the cost2goal for start node
    cost2goal[2*s[0]][2*s[1]][int(s[2]/30)] =  cos2goal(start,goal)

    #Updating the total heurisitc for start node
    totCost[2*s[0]][2*s[1]][int(s[2]/30)] = cost2come[2*s[0]][2*s[1]][int(s[2]/30)] + cost2goal[2*s[0]][2*s[1]][int(s[2]/30)]
    q.put([totCost[2*s[0]][2*s[1]][int(s[2]/30)], s])               #Initializing the queue with a Total cost and the start node
    
    for i in range(0, 401):
        for j in range(0, 301):
            for k in range(0,13):
                path_track[str([2*i, 2*j, k])] = []
    
    #print(path_track)
            
    start_time = time.time()    #Program start time
    main()
    #Time to reach goal state
    print('time to reach goal',time.time()-start_time)
    
    s=[2*s[0],2*s[1],int(s[2]/30)]
    g=[2*g[0],2*g[1],int(g[2]/30)]
    print(g)
    path_track_list = backtracking(s, g)
    
    path=[path_track_list[0],path_track_list[1]]
    print(path)
    for path in path_track_list:
        #time.sleep(0.00005)
        #pygame.time.wait(10)
        x = path[0]/2
        y = abs(300-path[1]/2)
        pygame.display.flip()
        pygame.draw.rect(gameDisplay, (255,35,0), [x,y,1,1])
        pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{im_count}.png")         #Saving the images to create a video                                                                                         #uncomment if not required
        im_count+=1
        pygame.time.wait(50)
    
    pygame.quit()
    #Printing the total time taken to reach goal state and backtrack
    print("total time:")
    print(time.time()-start_time)

   
#### Code Execution ends here #######
'''
#Writing to video. Uncomment if required
size=(400,300)
out = cv2.VideoWriter('p2dijkstrarigid.avi',cv2.VideoWriter_fourcc(*'DIVX'), 800, size)
file_list=os.listdir('/home/jayesh/Documents/ENPM661_PROJECT1/map1')
new_list=[]
for file in file_list:
    #print(file)
    a=file.split('.')[0]
    #print(a)
    new_list.append(a)
#print(new_list)
for i in range(0,len(new_list)):
    filename=f'/home/jayesh/Documents/ENPM661_PROJECT1/map1/{i}.png'
    #print(filename)
    j+=1
    #print(filename)
    img = cv2.imread(filename)
    out.write(img)
#cv2.imshow('obstacle',img)
out.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
'''