import os
import numpy as np
from Ques_1 import Ques_1
from blankTile import blankTile

"""Project 1: 15 Puzzle Challenge
This Project is about starting with a given instance of a 4X4 matrix
with numbers 1-15 and an empty tile, with the purpose being assorting
the numbers at the initial state to a sorted out list from 1-15 with the
empty tile being at the end.
"""

"""To better store and retrieve the nodes, a function that converts the nodes (matrices) 
into  a string is created here"""

def mat2Str(matrix):
    node_Str = ""
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            temp = str(matrix[i][j])
            if node_Str == "":
                node_Str=temp
            else: node_Str = node_Str + " " + temp

    return node_Str 

"""Here are the initial State stored as a matrix and continuous number
string variable"""
start_State_1 = np.array([[1, 2, 3, 4],[ 5, 6,0, 8], [9, 10, 7, 12] , [13, 14, 11, 15]])
start_State_Str_1 = mat2Str(start_State_1)

start_State_2 = np.array([[1, 0, 3, 4],[ 5, 2, 7, 8], [9, 6, 10, 11] , [13, 14, 15, 12]])
start_State_Str_2 = mat2Str(start_State_2)

start_State_3 = np.array([[0, 2, 3, 4],[ 1,5, 7, 8], [9, 6, 11, 12] , [13, 10, 14, 15]])
start_State_Str_3 = mat2Str(start_State_3)

start_State_4 = np.array([[5, 1, 2, 3],[0,6, 7, 4], [9, 10, 11, 8] , [13, 14, 15, 12]])
start_State_Str_4 = mat2Str(start_State_4)

start_State_5 = np.array([[1, 6, 2, 3], [9,5, 7, 4], [0, 10, 11, 8] , [13, 14, 15, 12]])
start_State_Str_5 = mat2Str(start_State_5)

test_Cases = [start_State_1, start_State_2, start_State_3, start_State_4, start_State_5]
test_Case_Strs = [start_State_Str_1, start_State_Str_2, start_State_Str_3, start_State_Str_4, start_State_Str_5]
"""Here is the Goal State also stored as a matrix"""

desired_State = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
desired_State_Str = mat2Str(desired_State)

"""Next a list that holds all of the visited state nodes is created"""

node_lib = []

"""Next blank tile (cell with value of zero) object is created to locate and move blank tile"""

bt = blankTile()

"""Then create a Que that stores nodes tracing desired state to the initial state"""

trace_Node = Ques_1()

"""Ques will be used to store status of layers being solved, ie the children 
of each parent node will be temporarily stored here"""

temp_list = Ques_1()        #<< Stores the temporary status of nodes/children during node expansion

node_State = []             #<< Saves the nodes of each state as a matrix during expansion 
node_State_Str = ""         #<< Saves the node state matrix as a string
parent_Child = []           #<< Stores each parent node and the expanded children for the entire Game

""" A dictionary is then created to store the node(matrix) and it's matching string to keep track
of the expanded children"""

node_State_Dict = {}        #<< Stores each expanded node matrix and its string version together

def main():
    parent_Child.clear()
    indx = 0 #child expansion counter
    while temp_list.size() > 0 and indx < 100000:
        
        node_State = temp_list.rem()
        node_State_Str = mat2Str(node_State)
        
        if node_State_Str == desired_State_Str:  #Check if node is equal to goal state
            node_State_Dict[node_State_Str] = node_State
            break 
        if node_State_Str in node_lib:
            continue
        
        node_lib.append(node_State_Str) # Nodes saved in a list as strings
        node_State_Dict[node_State_Str] = node_State #Node Matrix / String dictionary stored
        parent = node_State_Str # Store parent node as a string
        child = [] # Stores child nodes as list of strings

        blank_Cell = bt.getLocation(node_State)
        i = blank_Cell[0]; j= blank_Cell[1] #location of blank tile i-th row and j-th column

        now = bt.moveLeft(node_State, i, j)
        
        if len(now[0]) != 1:
            L = mat2Str(now)
        else:
            L = ""
        
        if L != node_State_Str and L != "":
            
            temp_list.add(now)
            
            child.append(mat2Str(L))
        
        now = bt.moveUp(node_State, i, j)
        
        if len(now[0]) != 1:
            U = mat2Str(now)
        else:
            U = ""
        
        if U != node_State_Str and U != "":
            
            temp_list.add(now)
            child.append(mat2Str(U))

        now = bt.moveRight(node_State, i, j)
        
        if len(now[0]) != 1:
            R = mat2Str(now)
        else:
            R=""
        if R != node_State_Str and R != "":
            temp_list.add(now)    
            child.append(mat2Str(R))
        
        now = bt.moveDown(node_State, i, j)
        
        if len(now[0]) != 1:
            D = mat2Str(now)
        else:
            D = ""
        if D != node_State_Str and D != "":
            temp_list.add(now)
            child.append(mat2Str(D))

        combo = [parent, child]
        parent_Child.append(combo)
        indx+=1
        print(indx)
    temp_list.is_empty()
    node_lib.clear()
    print("The node at the end of a " + str(indx) + " iteration expansion: " + node_State_Str + " is the same as the desired state")
    print(desired_State_Str)
    return node_State, node_State_Str

reached_State = []

def searchPath (path_lib, state_Str):       #<< Traces the path from initial to goal state once puzzle is solved
    trace_Node.is_empty()
    trace_Node.add(state_Str)
    node_State_Str = state_Str
    
    for i in range(len(path_lib)):
        parent=  path_lib[-i-1][0]
        child = []
        for j in range(len(path_lib[-i-1][1])):
            temp = path_lib[-i-1][1][j]
            b= temp.replace("   ", "_") 
            c = b.replace(" ", "")
            d = c.replace("_", " ")
            child.append(d)  
        if node_State_Str in child:
            node_State_Str = parent 
            trace_Node.add(node_State_Str)
                        
    return trace_Node.node


def writeFile(nodeNo, reached_State, test_State, path):         #<< Writes result for each test case on a separate text file
    txtFile= open("nodePath" + str(nodeNo) +".txt","w+")

    txtFile.write("The elements are being stored column-wise, i.e. for this state " + mat2Str(test_State) + "\n")
    txtFile.write("the fifteen puzzle state is: " +  "\n")
    for j in range(len(reached_State[0])):
        for k in range(len(reached_State[j])):
            txtFile.write(str(reached_State[j][k]) + " " )
        txtFile.write("\n")
    txtFile.write("The path of the nodes from start to finish is shown below as a string matrices, 0th - 15th number \n")
    
    # Entire path of solution is generated as a matrix from start to finish
    for i in range(len(path)):
        node = node_State_Dict[path[i]]
        txtFile.write("\n")
        txtFile.write("<< STEP "+ str(i) +" >> \n")    
        txtFile.write(str(node)+ "\n")
        txtFile.write("\n")
    txtFile.write("\n")
    txtFile.write("         CONGRATULAIONS!!! YOU'VE REACHED THE END OF 15 PUZZLE GAME!!!            ")        
    txtFile.close()

if __name__ == "__main__":          #Calls on the main method to solve puzzle after obtaining input from user. 
    
    j = True
    while j:
        
        print("")
        print("Hi and welcome to the 15 puzzle game!!!")
        print("")
        print("Listed below are the test case options in order (1-5):")
        print("")
        print(str(test_Cases[0]) + " <- Test Case 1") 
        print("")
        print(str(test_Cases[1]) + " <- Test Case 2") 
        print("")
        print(str(test_Cases[2]) + " <- Test Case 3")
        print("")
        print(str(test_Cases[3]) + " <- Test Case 4") 
        print("")
        print(str(test_Cases[4]) + " <- Test Case 5")
        print("")
        try:
            test_No = int(input("Type in which test case (1-5) you want to attempt: "))
        
            if test_No in [1,2,3,4,5]:
                
                print("Solving....")
                test = test_Cases[test_No-1]
                temp_list.node.append(test)
                reached_State, node_State_Str = main()
                puzzle_Path = searchPath(parent_Child, node_State_Str)
                print("The full search path from initial to desired end is stored in the nodePath" + str(test_No)+".txt file ")
                print("\n")
                writeFile(test_No, reached_State, test, puzzle_Path)
                attempt = int(input("Do you want to try another test case? Put 1 for 'Yes' or 0 for 'No thanks':  "))
                if attempt == 1:
                    continue
                elif attempt == 0:
                    print("")
                    print("Have a good one. Thanks for playing 15 puzzle game.")
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
            continue

os._exit(0)          