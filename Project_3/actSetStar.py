#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:24:26 2021
@author: jayesh
@teammate: Yoseph Kebede
"""


import numpy as np
import math 

class actionSet:
    
    #Function to traverse in the downward direction 
    #Degree = 30
    def ActionZero(self,curr_node,step):
        new_node=[]
        x = curr_node[0]
        y = curr_node[1]
        ang=curr_node[2]
        #print('act',x,y,ang)
        x1=round(2*(x+step*math.cos(ang*math.pi/180)))/2
        y1=round(2*(y+step*math.sin(ang*math.pi/180)))/2
        #print('act1',x1,y1,ang)       
        new_node=[int(x1),int(y1),ang]
        return new_node

    #Function to traverse in the upward direction
    def ActionP30(self,curr_node,degree,step):
        new_node=[]
        x = curr_node[0]
        y = curr_node[1]
        ang=curr_node[2]
        
        x1=round(2*(x+step*math.cos((ang+degree)*math.pi/180)))/2
        y1=round(2*(y+step*math.sin((ang+degree)*math.pi/180)))/2
        
        if ang+degree>=360:
            new_node=[int(x1),int(y1),int(ang+degree-360)]
        elif ang+degree<0:
            new_node=[int(x1),int(y1),int(ang+degree+360)]
        else:
            new_node = [int(x1),int(y1),int(degree+ang)]        
        
        return new_node

    #Function to traverse to the left
    def ActionP60(self,curr_node,degree,step):
        new_node=[]
        x = curr_node[0]
        y = curr_node[1]
        ang=curr_node[2]
        
        x1=round(2*(x+step*math.cos((ang+2*degree)*math.pi/180)))/2
        y1=round(2*(y+step*math.sin((ang+2*degree)*math.pi/180)))/2
        
        if ang+degree>=360:
            new_node=[int(x1),int(y1),int((ang+(2*degree))-360)]
        elif ang+degree<0:
            new_node=[int(x1),int(y1),int((ang+(2*degree))+360)]
        else:
            new_node = [int(x1),int(y1),int(2*degree+ang)]        
        
        return new_node

    #Function to traverse to the right
    def ActionN30(self,curr_node,degree,step):
        new_node=[]
        x = curr_node[0]
        y = curr_node[1]
        ang=curr_node[2]
        
        x1=round(2*(x+step*math.cos((ang-degree)*math.pi/180)))/2
        y1=round(2*(y+step*math.sin((ang-degree)*math.pi/180)))/2
                  
        if ang<degree:
            new_node=[int(x1),int(y1),int((ang+360-degree))]
        else:
            new_node = [int(x1),int(y1),int(-degree+ang)] 
        
        return new_node
    
    #Function to traverse in the upward left direction
    def ActionN60(self,curr_node,degree,step):
        new_node=[]
        x = curr_node[0]
        y = curr_node[1]
        ang=curr_node[2]
        
        x1=round(2*(x+step*math.cos((ang-2*degree)*math.pi/180)))/2
        y1=round(2*(y+step*math.sin((ang-2*degree)*math.pi/180)))/2
        
        if ang<2*degree:
            new_node=[int(x1),int(y1),int((ang-2*degree)+360)]
        else:
            new_node = [int(x1),int(y1),int(-2*degree+ang)]      
        
        return new_node
    

    #Function run initially to set the obstacle coordinates in the image and append to a list
    def getobstaclespace(self):
        oblist1=[]       #List to store the obstacle coordinates for final animation
        riglist=set([])
        radius=10
        clearance=5
        dist= radius + clearance
        xmax=100
        ymax=100
        #print('ob space')
        for x in range(0,10):
            for y in range(0,10):
                
                #Center Circle
                if ((x-xmax/2)**2 + (y-ymax/2)**2 < (10)**2):
                    oblist1.append([x,y])

                if ((x-xmax/2)**2 + (y-ymax/2)**2 < (10+dist)**2):
                    riglist.add(str([x,y]))

                #Left Bottom Circle
                if ((x-30)**2 + (y-20)**2 < 10**2):
                    oblist1.append([x,y])

                if ((x-30)**2 + (y-20)**2 < (10+dist)**2):
                    riglist.add(str([x,y]))

                #Right Bottom Circle
                if ((x-70)**2 + (y-20)**2 < 10**2):
                    oblist1.append([x,y])

                if ((x-70)**2 + (y-20)**2 < (10+dist)**2):
                    riglist.add(str([x,y]))

                #Right Top Circle
                if ((x-70)**2 + (y-80)**2 < 10**2):
                    oblist1.append([x,y])

                if ((x-70)**2 + (y-80)**2 < (10+dist)**2):
                    riglist.add(str([x,y]))

                #Left Square
                if (x>=2.5 and x<=17.5) and (y>=42.5 and y<=57.5):
                    oblist1.append([x,y])

                if (x>=2.5-dist and x<=17.5+dist) and (y>=42.5-dist and y<=57.5+dist):
                    riglist.add(str([x,y]))

                #Right Square
                if (x>=82.5 and x<=97.5) and (y>=42.5 and y<=57.5):
                    oblist1.append([x,y])

                if (x>=82.5-dist and x<=97.5+dist) and (y>=42.5-dist and y<=57.5+dist):
                    riglist.add(str([x,y]))

                #Left Top Square
                if (x>=22.5 and x<=37.5) and (y>=72.5 and y<=87.5):
                    oblist1.append([x,y])

                if (x>=22.5-dist and x<=37.5+dist) and (y>=72.5-dist and y<=87.5+dist):
                    riglist.add(str([x,y]))

                # #Rectangular Object
                # if y-0.7*x>=74.28 and y-0.7*x <= 98.76 and y+1.425*x>=176.42 and y+1.428*x<=438.045:
                #     oblist1.append([x,y])   
                    
                # if y>=(x-44.316)*math.tan(35*math.pi/180)+87.109 and y <= (x-15.6376)*math.tan(35*math.pi/180)+128.066 and y>=-math.tan(55*math.pi/180)*(x-15.637)+128.066 and y<=-math.tan(55*math.pi/180)*(x-163.084)+231.31:
                #         riglist.add(str([x,y]))

                # #Circle Object
                # if ((x-90)**2 + (y-70)**2)<(35**2):
                #     oblist1.append([x,y])
                
                # if ((x-90)**2 + (y-70)**2)<((35+dist)**2):
                #     riglist.add(str([x,y]))
                
                # #Ellipse Object
                # if(((x-246)**2)/(60)**2 +((y-145)**2)/(30)**2 <= 1):
                #     oblist1.append([x,y])
            
                # if(((x-246)**2)/(60+dist)**2 +((y-145)**2)/(30+dist)**2 <= 1):
                #     riglist.add(str([x,y]))
                
                # #Polygon Shaped Object
                # if (x>=200 and x<=230) and (y>=230 and y<=280):    
                #     if (x>=200 and x<=210 and y>=240 and y<=270):
                #         oblist1.append([x,y])
                #     if (y>=270 and y<=280 and x>=210 and x<=230):
                #         oblist1.append([x,y])
                #     if (y>=230 and y<=240 and x>=210 and x<=240):
                #         oblist1.append([x,y])
                #     if (x<=210 and y<=240):
                #         oblist1.append([x,y])
                #     if (x<=210 and y>=270 and y<=280):
                #         oblist1.append([x,y])
                    
                # if (x>=200-dist and x<=230+dist) and (y>=230-dist and y<=280+dist):    
                #     if (x>=200-dist and x<=210+dist and y>=240-dist and y<=270+dist):
                #         riglist.add(str([x,y]))
                #     if (y>=270-dist and y<=280+dist and x>=210-dist and x<=230+dist):
                #         riglist.add(str([x,y]))
                #     if (y>=230-dist and y<=240+dist and x>=210-dist and x<=240+dist):
                #         riglist.add(str([x,y]))
                #     if (x<=210+dist and y<=240+dist):
                #         riglist.add(str([x,y]))
                #     if (x<=210+dist and y>=270-dist and y<=280+dist):
                #         riglist.add(str([x,y]))
            
                #Resolution Check
                if x>=0 and x<=dist:
                    riglist.add(str([x,y]))
                
                if y>=0 and y<=dist:
                    riglist.add(str([x,y])) 
               
                if x>=(xmax-dist) and x<=xmax:
                    riglist.add(str([x,y]))
                
                if y>=(ymax-dist) and y<=ymax:
                    riglist.add(str([x,y]))
                        
        return oblist1,riglist