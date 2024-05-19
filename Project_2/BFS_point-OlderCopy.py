import os
import cv2
import time
import math 
from PIL import Image
import numpy as np
from Ques_1 import Ques_1
from actionSet import actionSet
from actionSet import obstacleSpace

""" References: Besides researching over the internet on implementation of cv2, I have referenced one approach
in depicting images from numpy arrays and backtracking optimal path from Divyam's (ENPM661 TA's) Dijkstra algorithm 
of point robot search.
github link: https://github.com/divi9626/Djikstra-Implementation/blob/master/Djikstra_point
"""
"""Project 2: Implementation of Breadth First Search (BFS) algorithm for a Point Robot
This Project use the BFS algorithm to find a point robot in a space with obstacles
The goal is to use 8 action steps to search the environment beginning from the initial 
point assigned by the user and expand until goal state is reached. Then by using backward
search, the optimal path is traced.
"""
"""Have the user enter the starting point for all 0 <= x <= 400 and 0<= y <= 300 """

"""Here are the initial State stored as a matrix and continuous number
string variable"""
start_State_1 = [0,0]

start_State_2 = [7,10]

test_Cases = [start_State_1, start_State_2]
"""Here is the Goal State also stored as a matrix"""

desired_State = [48, 160]#[125,50] #[90,120]#[125,50]#

"""Next a list that holds all of the visited state nodes is created"""

node_lib = []

"""Next blank tile (cell with value of zero) object is created to locate and move blank tile"""

bt = actionSet()
oS = obstacleSpace()

"""Then create a Que that stores nodes tracing desired state to the initial state"""

trace_Node = Ques_1()

"""Ques will be used to store status of layers being solved, ie the children 
of each parent node will be temporarily stored here"""

temp_list = Ques_1()        #<< Stores the temporary status of nodes/children during node expansion

node_State = []             #<< Saves the nodes of each state as a matrix during expansion 
parent_Child = []           #<< Stores each parent node and the expanded children for the entire Game
combo = {}
#start_Node = []
"""Image Processing define assignments for displaying results in animation"""
width, height = 400, 300 
frame = np.zeros([height, width, 3], dtype=np.uint8)

def obstacleRegion():
    
    for x in range(width):
        for y in range(height):
            node = [x, y]
            if oS.circleSpace(node):
                frame[height-1-y, x] = (128, 128, 128)
            if oS.rectangleSpace(node):
                frame[height-1-y, x] = (200, 128, 0)
            if oS.ellipseSpace(node):
                frame[height-1-y, x] = (0, 128, 200)
            if oS.enclosedSpace(node):
                frame[height-1-y, x] = (255, 0, 80)
            if oS.cShapeSpace(node):
                frame[height-1-y, x] = (200, 200, 200)
    
def obstacleSpace(node_State):
    if oS.circleSpace(node_State):
        return False
    if oS.rectangleSpace(node_State):
        return False
    if oS.ellipseSpace(node_State):
        return False
    if oS.enclosedSpace(node_State):
        return False
    if oS.cShapeSpace(node_State):
        return False
    return True

def main(start_Node):
    parent_Child.clear()
    indx = 0 #child expansion counter
    #start_Node = temp_list.rem()
    combo[(start_Node[0],start_Node[1])] = None
    #combo[None] = (start_Node[0],start_Node[1])
    print("In main")
    while temp_list.size() > 0 and indx < 100000:
        #print("In while loop")
        node_State = temp_list.rem()
        parent = node_State
        child = [] # Stores child nodes as list of strings
        

        now = bt.moveLeft(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveUpLeft(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveUp(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveUpRight(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveRight(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveDownRight(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveDown(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                #child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
            
        now = bt.moveDownLeft(node_State)
        if now is not None:
            if now not in node_lib and (now not in temp_list.node) and obstacleSpace(now): 
                temp_list.add(now) 
                #child.append(now)
                #combo[(parent[0],parent[1])] = (now[0],now[1])
                combo[(now[0],now[1])] = (parent[0],parent[1])
        
        """check if node is in visited list"""
        if node_State in node_lib:
            continue

        node_lib.append(node_State) # Nodes saved in visited list
        
        if parent == desired_State:  #Check if node is equal to goal state
            break 
        
        #combo_list = [parent, child]
        #parent_Child.append(combo_list)
        indx+=1
        #print(indx)
        print(parent)
    print(combo)    
    temp_list.is_empty()
    print("The node at the end of a " + str(indx) + " iteration expansion: " + str(node_State) + " is the same as the desired state")
    print(desired_State)
    return node_State

reached_State = []

def searchPath (state_Node, initial_Node):       #<< Traces the path from initial to goal state once puzzle is solved
    trace_Node.is_empty()
    #optimal_path = []
    #optimal_path.append((state_Node[0],state_Node[1]))
    x,y = state_Node[0],state_Node[1]
    parent = (x, y)#combo[(state_Node[0],state_Node[1])]
    trace_Node.add((x, y))#(state_Node[0],state_Node[1]))
    #parent_old = (-1,-1)
    print(parent)
    #node_State = state_Node
    
    while parent is not None:#!= (initial_Node[0], initial_Node[1]):#None:
        #parent_old = parent
        trace_Node.add(parent)
        #optimal_path.append(parent)
        parent = combo[parent]
        # if parent_old == parent:
        #     break
        
        # if parent == (0,0):#30):
        #     break
        print(parent)
    #trace_Node.add((initial_Node[0], initial_Node[1]))
    # for i in range(len(parent_Child)):
    #     parent=  parent_Child[-i-1][0]
    #     child = []
    #     for j in range(len(parent_Child[-i-1][1])):
    #         temp = parent_Child[-i-1][1][j]
    #         child.append(temp)  
    #         if node_State in child:
    #             node_State = parent 
    #             trace_Node.add(node_State)
    #     print(parent)                
    return trace_Node.node#optimal_path#

def imageDraw (full_Path, optimal_path, start_Node, goal_Node):
    frame[height-1-start_Node[1], start_Node[0]] = (255, 165, 0)
    frame[height-1-goal_Node[1], goal_Node[0]] = (255, 0, 0)

    for list in full_Path:
        y = list[1]
        x = list[0]
        
        frame[height-1-y, x]= (255, 255, 255) 
        
        cv2.imshow('Search Map', frame)
        if cv2.waitKey(1) == 49:
            break
    for node in optimal_path:
        frame[height-1-node[1], node[0]] = (255, 0, 0)
   
    cv2.imshow('Search Map', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# def writeFile(nodeNo, reached_State, test_State, path):         #<< Writes result for each test case on a separate text file
#     txtFile= open("nodePath" + str(nodeNo) +".txt","w+")

#     txtFile.write("The point robot is being searched beginning from location: " + str(test_State) + "\n")
#     txtFile.write("the goal state is located at point : " +  "\n")
#     txtFile.write(str(reached_State) + " " )
#     txtFile.write("\n")
#     txtFile.write("The path of the nodes from start to finish is shown below as a string of coordinate points [x,y] \n")
    
#     # Entire path of solution is generated as a matrix from start to finish
#     for i in range(len(path)):
#         node = path[i]
#         txtFile.write("\n")
#         txtFile.write("<< STEP "+ str(i) +" >> \n")    
#         txtFile.write(str(node)+ "\n")
#         txtFile.write("\n")
#     txtFile.write("\n")
#     txtFile.write("         CONGRATULAIONS!!! YOU'VE LOCATED THE POINT ROBOT AND IT'S OPTIMAL PATH!!!            ")        
#     txtFile.close()

if __name__ == "__main__":          #Calls on the main method to solve puzzle after obtaining input from user. 
    
    image = cv2.imread(r'D:\Documents\UMD_Docs\Grad-school\ENPM661\Project_2\Map-updated_dimentions.png')
        #Read Image from Path
    
    j = True
    while j:
       
        print("")
        print("Hi and welcome to the 'Find the Point Robot Game'!!!")
        print("")
        print("The point robot is hidden somewhere in this map. The goal is to input a start node to start your search")
        print("Press any key to continue....")
        cv2.imshow("Map", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("")
        print("Listed below are the test case options in order (1-2):")
        print("")
        print(str(test_Cases[0]) + " <- Test Case 1") 
        print("")
        print(str(test_Cases[1]) + " <- Test Case 2") 
        print("")
        print("You can either choose the initial nodes from above or enter new starting node")
        print("")
        try:
            selection = int(input("Would you like to choose from test cases or enter new node? Enter '1' for test cases or '2' for new node: "))
            test = []
            test_No = 0
            if selection == 1:
                test_No = int(input("Type in which test case 1 or 2 you want to attempt: "))
                test = test_Cases[test_No-1]
                print(test)
            elif selection == 2:
                x= int(input("Enter the x coordinate of your start point from [0-400]: "))
                y= int(input("Enter the y coordinate of your start point from [0-300]: "))
                test = [x, y]
                print(test)
            
            if not obstacleSpace(test):
                print("Entered node is in obstacle space try again!")
                continue
            
            if selection == 1 or selection == 2:    
                print("Solving....")
                temp_list.add(test)
                #start_Node = test
                reached_State= main(test)
                puzzle_Path = searchPath(reached_State, test)
                #print(puzzle_Path)
                print("The full search path from initial to desired end is stored in the nodePath" + str(test_No)+".txt file ")
                print("\n")
                #writeFile(test_No, reached_State, test, puzzle_Path)
                print("")
                print("Processing image...")
                obstacleRegion()
                print("Here is what the recreated environment looks like. Press any key to see the search in animation....")
                print("")
                begin = input("Type in which any letter to start animation:  ")
                 
                imageDraw(node_lib, puzzle_Path, test, desired_State)
                #waits for user to press any key  
                 
                attempt = int(input("Do you want to try another test case? Put 1 for 'Yes' or 0 for 'No thanks':  "))
                if attempt == 1:
                    node_lib.clear()
                    cv2.destroyAllWindows()  
                    continue
                elif attempt == 0:
                    print("")
                    print("Have a good one. Thanks for playing 'Find the Point Robot'.")
                    print("")  
                    j = False
                else:
                    print("")
                    print("Incorrect entry. Goodbye!")
                    print("")
                    break
            else:
                print("Wrong entry. Try Again!")
        except ValueError:
            print("Entered wrong value. Try again.")
            raise
            continue
#closing all open windows  
cv2.destroyAllWindows()  
os._exit(0)          


{1:2,1:3,1:4, 2:1,2:4,2:5}