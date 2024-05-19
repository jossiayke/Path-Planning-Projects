#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 06:44:49 2021
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

#Creating an image to use for animation
img = np.zeros((301, 401), np.uint8)

oblist=set([])   #Set to store the obstacle coordinates
oblist1=[]       #List to store the obstacle coordinates for final animation
riglist=set([])
radius=10
clearance=5
dist=radius+clearance
xmax=400                    #Width of the map
ymax=300                    #Height of the map

#Function to traverse in the downward direction
def ActionMoveDown(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_y = int(curr_node[1])
    new_node_y-=1
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,1

#Function to traverse in the upward direction
def ActionMoveUp(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_y = int(curr_node[1])
    new_node_y+=1
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,1

#Function to traverse to the left
def ActionMoveLeft(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_x-=1
    new_node_y = int(curr_node[1])
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,1

#Function to traverse to the right
def ActionMoveRight(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_x+=1
    new_node_y = int(curr_node[1])
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,1
    
#Function to traverse in the upward left direction
def ActionMoveUL(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_x -=1
    new_node_y = int(curr_node[1])
    new_node_y+=1
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,math.sqrt(2)
    
#Function to traverse in the upward right direction
def ActionMoveUR(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_x+= 1
    new_node_y = int(curr_node[1])
    new_node_y+= 1
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,math.sqrt(2)

#Function to traverse in the downward left direction
def ActionMoveDL(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_x-=1
    new_node_y = int(curr_node[1])
    new_node_y-=1
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,math.sqrt(2)

#Function to traverse in the downward right direction
def ActionMoveDR(curr_node,cost):
    new_node=[]
    new_node_x = int(curr_node[0])
    new_node_x+=1
    new_node_y = int(curr_node[1])
    new_node_y-=1
    new_node = [new_node_x,new_node_y]
    if new_node[0]>=0 and new_node[1]>=0:
        return new_node,math.sqrt(2)

#Function run initially to set the obstacle coordinates in the image and append to a list
def getobstaclespace():
    #print('ob space')
    for x in range(0,401):
        for y in range(0,301):
            
            #Rectangular Object
            if y-0.7*x>=74.28 and y-0.7*x <= 98.76 and y+1.425*x>=176.42 and y+1.428*x<=438.045:
                img[y][x]=255
                oblist.add(str([x,y]))
                oblist1.append([x,y])   

            if y>=(x-44.316)*math.tan(35*math.pi/180)+87.109 and y <= (x-15.6376)*math.tan(35*math.pi/180)+128.066 and y>=-math.tan(55*math.pi/180)*(x-15.637)+128.066 and y<=-math.tan(55*math.pi/180)*(x-163.084)+231.31:
                riglist.add(str([x,y]))

            #Circle Object
            if ((x-90)**2 + (y-70)**2)<(35**2):
                img[y][x]=255
                oblist.add(str([x,y]))
                oblist1.append([x,y])
                
            if ((x-90)**2 + (y-70)**2)<((35+dist)**2):
                riglist.add(str([x,y]))
                
            #Ellipse Object
            if(((x-246)**2)/(60)**2 +((y-145)**2)/(30)**2 <= 1):
                img[y][x]=255
                oblist.add(str([x,y]))
                oblist1.append([x,y])
            
            if(((x-246)**2)/(60+dist)**2 +((y-145)**2)/(30+dist)**2 <= 1):
                riglist.add(str([x,y]))
                
            #Polygon Shaped Object
            if (x>=200 and x<=230) and (y>=230 and y<=280):    
                if (x>=200 and x<=210 and y>=240 and y<=270):
                    img[y][x]=255
                    oblist.add(str([x,y]))
                    oblist1.append([x,y])
                if (y>=270 and y<=280 and x>=210 and x<=230):
                    img[y][x]=255
                    oblist.add(str([x,y]))
                    oblist1.append([x,y])
                if (y>=230 and y<=240 and x>=210 and x<=240):
                    img[y][x]=255
                    oblist.add(str([x,y]))
                    oblist1.append([x,y])
                if (x<=210 and y<=240):
                    img[y][x]=255
                    oblist.add(str([x,y]))
                    oblist1.append([x,y])
                if (x<=210 and y>=270 and y<=280):
                    img[y][x]=255
                    oblist.add(str([x,y]))
                    oblist1.append([x,y])
                    
            if (x>=200-dist and x<=230+dist) and (y>=230-dist and y<=280+dist):    
                if (x>=200-dist and x<=210+dist and y>=240-dist and y<=270+dist):
                    riglist.add(str([x,y]))
                if (y>=270-dist and y<=280+dist and x>=210-dist and x<=230+dist):
                    riglist.add(str([x,y]))
                if (y>=230-dist and y<=240+dist and x>=210-dist and x<=240+dist):
                    riglist.add(str([x,y]))
                if (x<=210+dist and y<=240+dist):
                    riglist.add(str([x,y]))
                if (x<=210+dist and y>=270-dist and y<=280+dist):
                    riglist.add(str([x,y]))
            
            #Resolution Check
            if x>=0 and x<=dist:
                riglist.add(str([x,y]))
                
            if y>=0 and y<=dist:
                riglist.add(str([x,y])) 
               
            if x>=(xmax-dist) and x<=xmax:
                riglist.add(str([x,y]))
                
            if y>=(ymax-dist)and y<=ymax:
                riglist.add(str([x,y]))
            


        

getobstaclespace()
#s = [1,1]                   #Start Position Test Case1
#g = [399,299]               #Goal Position Test Case1
xmax=400                    #Width of the map
ymax=300                    #Height of the map
solvable=False
visited_nodes = set([])     #Set consisting of all the nodes traversed by the point robot
visited=[]                  #Containing the list of visited nodes. Would be used for animating the visited states in the map
child_node = []             #stores the child states after point robot moves to different positions
path_track={}               #Dictionary storing the parent nodes of the different child nodes to backtrack the path followed

l=0
q = PriorityQueue()         #Setting a priority queue
distance = {}               #Dictionary to store the distance of a node from the previous node 

def cost_update(child,loc,cost):
    #Checking if the child nodes are visited or not, if they lie within the resolution specified and if present in the obstacle space
    if (str(child) not in riglist) and (child[0]>0 and child[0]<xmax) and (child[1]>0 and child[1]<ymax) and (child is not None):
        if (str(child) in visited_nodes):
            new_cost=cost+distance[str(loc)]
            if new_cost < distance[str(child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
                distance[str(child)] = new_cost
        else:
            visited_nodes.add(str(child))         #Adding the child nodes to the set of visited nodes
            visited.append(child)
            new_cost=cost+distance[str(loc)]      #Calculating the new cost
            distance[str(child)]=new_cost         #Setting the new cost of the node
            q.put([new_cost, child])              #Updating the priority queue
            path_track[str(loc)].append(child)   #Updating the parent information
            

#Setting the cost of the start node to 0

 
def main():
#if solvable:
    #print('solvable')
    while not q.empty():  #Process when queue is not empty
        print(l)
        a=q.get()         #Varibale to store the cost and node position
        #print('queue',a[0],a[1],len(a))
        
        #Checking if goal is reached or not
        if a[1]==g:
            print('goal reached')
            break

        l+=1
        
        visited.append(a[1])

        #Inititalizing the dictionary to store information related to the parent node
        path_track[str(a[1])] = []

        #Getting the child nodes after moving in different positions
        l_child,cost1 = ActionMoveLeft(a[1],a[0])
        cost_update(l_child, a[1], cost1)
        u_child,cost2 = ActionMoveUp(a[1],a[0])
        cost_update(u_child, a[1], cost2)
        r_child,cost3= ActionMoveRight(a[1],a[0])
        cost_update(r_child, a[1], cost3)
        d_child,cost4 = ActionMoveDown(a[1],a[0])
        cost_update(d_child, a[1], cost4)
        ul_child,cost5 = ActionMoveUL(a[1],a[0])
        cost_update(ul_child, a[1], cost5)
        ur_child,cost6 = ActionMoveUR(a[1],a[0])
        cost_update(ur_child, a[1], cost6)
        dl_child,cost7 = ActionMoveDL(a[1],a[0])
        cost_update(dl_child, a[1], cost7)
        dr_child,cost8 = ActionMoveDR(a[1],a[0])
        cost_update(dr_child, a[1], cost8)
                    
               
        # #Checking if the child nodes are visited or not, if they lie within the resolution specified and if present in the obstacle space
        # if (str(l_child) not in riglist) and (l_child[0]>0 and l_child[0]<xmax) and (l_child[1]>0 and l_child[1]<ymax and l_child is not None):
        #     #cost_update(l_child,a[1])

        #     if (str(l_child) in visited_nodes):
                
        #         new_cost=cost1+distance[str(a[1])]
        #         if new_cost < distance[str(l_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(l_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(l_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(l_child)
        #         new_cost=cost1+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(l_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, l_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(l_child)   #Updating the parent information

        # #Similarly perform for the remaining nodes in different directions
        # if (str(r_child) not in riglist) and (r_child[0]>0 and r_child[0]<xmax) and (r_child[1]>0 and r_child[1]<ymax and r_child is not None):
        #     #cost_update(r_child,a[1])

        #     if (str(r_child) in visited_nodes):
        #         new_cost=cost2+distance[str(a[1])]
        #         if new_cost < distance[str(r_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(r_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(r_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(r_child)
        #         new_cost=cost2+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(r_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, r_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(r_child)   #Updating the parent information
   
        # if (str(u_child) not in riglist) and (u_child[0]>0 and u_child[0]<xmax) and (u_child[1]>0 and u_child[1]<ymax and u_child is not None):
        #     #cost_update(u_child,a[1])

        #     if (str(u_child) in visited_nodes):
        #         new_cost=cost3+distance[str(a[1])]
        #         if new_cost < distance[str(u_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(u_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(u_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(u_child)
        #         new_cost=cost3+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(u_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, u_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(u_child)   #Updating the parent information

        # if (str(d_child) not in riglist) and (d_child[0]>0 and d_child[0]<xmax) and (d_child[1]>0 and d_child[1]<ymax and d_child is not None):
        #     #cost_update(d_child,a[1])

        #     if (str(d_child) in visited_nodes):
        #         new_cost=cost4+distance[str(a[1])]
        #         if new_cost < distance[str(d_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(d_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(d_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(d_child)
        #         new_cost=cost4+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(d_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, d_child])              #Updating the priority queue
   
        # if (str(ul_child) not in riglist) and (ul_child[0]>0 and ul_child[0]<xmax) and (ul_child[1]>0 and ul_child[1]<ymax and ul_child is not None):
        #     #cost_update(ul_child,a[1])

        #     if (str(ul_child) in visited_nodes):
        #         new_cost=cost5+distance[str(a[1])]
        #         if new_cost < distance[str(ul_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(ul_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(ul_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(ul_child)
        #         new_cost=cost5+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(ul_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, ul_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(ul_child)   #Updating the parent information

        # if (str(dl_child) not in riglist) and (dl_child[0]>0 and dl_child[0]<xmax) and (dl_child[1]>0 and dl_child[1]<ymax and dl_child is not None):
        #     #cost_update(dl_child,a[1])

        #     if (str(dl_child) in visited_nodes):
        #         new_cost=cost6+distance[str(a[1])]
        #         if new_cost < distance[str(dl_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(dl_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(dl_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(dl_child)
        #         new_cost=cost6+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(dl_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, dl_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(dl_child)   #Updating the parent information

        # if (str(ur_child) not in riglist) and (ur_child[0]>0 and ur_child[0]<xmax) and (ur_child[1]>0 and ur_child[1]<ymax and ur_child is not None):
        #     #cost_update(ur_child,a[1])

        #     if (str(ur_child) in visited_nodes):
        #         new_cost=cost7+distance[str(a[1])]
        #         if new_cost < distance[str(ur_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(ur_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(ur_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(ur_child)
        #         new_cost=cost7+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(l_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, ur_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(ur_child)   #Updating the parent information

        # if (str(dr_child) not in riglist) and (dr_child[0]>0 and dr_child[0]<xmax) and (dr_child[1]>0 and dr_child[1]<ymax and dr_child is not None):
        #     #cost_update(dr_child,a[1])

        #     if (str(dr_child) in visited_nodes):
        #         new_cost=cost8+distance[str(a[1])]
        #         if new_cost < distance[str(dr_child)]:   #If node already visited updating the node with the new cost if new cost is less than the original value
        #             distance[str(dr_child)] = new_cost
        #     else:
        #         visited_nodes.add(str(dr_child))         #Adding the child nodes to the set of visited nodes
        #         visited.append(dr_child)
        #         new_cost=cost8+distance[str(a[1])]      #Calculating the new cost
        #         distance[str(dr_child)]=new_cost         #Setting the new cost of the node
        #         q.put([new_cost, dr_child])              #Updating the priority queue
        #         path_track[str(a[1])].append(dr_child)   #Updating the parent information

        #cv2.imshow('maze',img)
        #cv2.waitKey(1)

def backtracking (start, goal):
    #Backtracking to find the paths traversed from the initial state to the final state
    final_state = g
    val = g
    goal = s
    path_track_list=[]
    #print('Parent track',path_track)
    while val!=goal:
        for key, values in path_track.items():
            #print('key',key,values)
            while val in values:
                key= ast.literal_eval(key) #converting strings of lists to pure lists
                val = key
                path_track_list.append(val)
    path_track_list=path_track_list[::-1]
    path_track_list.append(final_state) 

    return path_track_list

def visualization(path_track_list):
    #Creating an animation using pygame
    pygame.init()

    display_width = 400
    display_height = 300

    gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.SCALED)
    pygame.display.set_caption('Djikstra Animation')

    black = (0,0,0)         #Color represnting the background of image
    white = (0,255,255)     #Color respresenting the visited nodes
    yellow=(255,255,0)      #Color representing the obstacles

    i=0
    #surf = pygame.surfarray.make_surface(img)

    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:  
                done = True   
        
        gameDisplay.fill(black)

        #Setting the obstacle space in the animation
        for path in oblist1:
                x = int(path[0])
                y = abs(300-int(path[1]))
                pygame.draw.rect(gameDisplay, yellow, [x,y,1,1])
        
        #print('Visited',visited)
        #Visualizing the visited states in the animation
        for path in visited:    
                x =path[0]
                y = abs(300-path[1])
                pygame.display.flip()
                pygame.draw.rect(gameDisplay, white, [x,y,1,1])
                #pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{i}.png")  #Saving the images to create a video 
                #i+=1                                                                                     #uncomment if not required
                pygame.time.wait(0)                    
        
        #Visualizing the path taken from start to node
        for path in path_track_list:
            pygame.time.wait(10)
            #time.sleep(0.00005)
            x = path[0]
            y = abs(300-path[1])
            pygame.display.flip()
            pygame.draw.rect(gameDisplay, (255,5,5), [x,y,1,1])
            #pygame.image.save(gameDisplay, f"/home/jayesh/Documents/ENPM661_PROJECT1/map1/{i}.png")         #Saving the images to create a video
            i+=1                                                                                            #uncomment if not required
            pygame.time.wait(10)
    
        done = True

    pygame.quit()

#### Code execution starts here #####
if __name__ == "__main__":
    start_time = time.time()    #Program start time
    while True:
        x1=int(input('Enter x coordinate of start node'))
        y1=int(input('Enter y coordinate of start node'))

        s = [x1,y1]
        x2=int(input('Enter x coordinate of goal node'))
        y2=int(input('Enter y coordinate of goal node'))
        g = [x2,y2]                 #Goal Position Test Case2  
        
        if s == g:  #Checking if goal node is the same as the start node
            print('goal node equal to start node. Re enter your points again')
            continue
        
        elif str(s) in riglist or str(g) in riglist: #checking if the goal or start node is in the obstaclespace including radius and clearance
            print('Starting or goal node in obstacle space. Re enter the points again')
            continue
        
        elif (s[0] <0 or s[0]> xmax) or (s[1]<0 or s[1] > ymax) or (g[0] <0 or g[0]> xmax) or (g[1]<0 or g[1] > ymax): #Checking if the start and goal node is within the grid(400x300)
            print('start/goal < 0 or greater than grid size. Re enter the points again')
            
        else:
            break
    print(s)                    
    print(g)
    q.put([0, s])               #Initializing the queue with a cost of 0 and the start node
    visited_nodes.add(str(s)) #Adding the start node to the set of visited nodes
    visited.append(s)         #Appending the visited list

    #Initializing the cost of all the points to infinity
    for i in range(0, xmax):
        for j in range(0, ymax):
            distance[str([i, j])] = 99999999 
    distance[str(s)] = 0 

    main()   
    #Time to reach goal state
    print(time.time()-start_time)

    path_track_list = backtracking(s, g)
    #Printing the total time taken to reach goal state and backtrack
    print("total time:")
    print(time.time()-start_time)  

    visualization(path_track_list)
#### Code Execution ends here #######

#Writing to video. Uncomment if required
'''
size=(400,300)
out = cv2.VideoWriter('p2dijkstra.avi',cv2.VideoWriter_fourcc(*'DIVX'), 800, size)
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