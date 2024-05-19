import numpy as np
import math 

class actionSet:

    # def __init__(self):

    #     self.matrix = []

    def moveLeft(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if x > 0 and x <= 400 :
            temp[0]= x-1
            return temp 
        else:
            return None

    def moveRight(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if x >= 0 and x < 400 :
            temp[0]= x+1
            return temp 
        else:
            return None

    def moveUp(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if y >= 0 and y < 300 :
            temp[1]= y+1
            return temp 
        else:
            return None

    def moveDown(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if y > 0 and y <= 300 :
            temp[1]= y-1
            return temp 
        else:
            return None

    def moveUpRight(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if x >= 0 and x < 400 and y >= 0 and y < 300 :
            temp[0] = x+1
            temp[1]= y+1
            return temp     
        else:
            return None
    def moveDownRight(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if x >= 0 and x < 400 and y > 0 and y <= 300 :
            temp[0] = x+1
            temp[1]= y-1
            return temp 
        else:
            return None

    def moveUpLeft(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if x > 0 and x <= 400 and y >= 0 and y < 300 :
            temp[0] = x-1
            temp[1]= y+1
            return temp 
        else:
            return None
    
    def moveDownLeft(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        if x > 0 and x <= 400 and y > 0 and y <= 300 :
            temp[0] = x-1
            temp[1]= y-1
            return temp 
        else:
            return None

class obstacleSpace:

    def circleSpace(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        #print("inside circle method")
        if (x-90)**2 + (y-70)**2 <= 35**2:
        #if (x <= math.sqrt(35**2-(y-70)**2)+90) and (y >= math.sqrt(35**2 - (x-90)**2) + 70):
            return True
        else:  
            return False
    
    def rectangleSpace(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        eq = [0,0,0,0]
        #if x <= (y - 108)/math.tan(35*math.pi/180) + 48:# and 
        if y >= (x-48)*math.tan(35*math.pi/180)+108:
            eq[0] = 1
        #if (x >= y - (108+20*math.sin(55*math.pi/180))/math.tan(35*math.pi/180) + (48+20*math.cos(55*math.pi/180))):# and 
        if y <= (x-(48-20*math.cos(55*math.pi/180)))*math.tan(35*math.pi/180) + 108+20*math.sin(55*math.pi/180):
            eq[1] = 1
        #if (x >= (y-(108+20*math.sin(55*math.pi/180)))*(-1)/math.tan(55*math.pi/180) + 48-20*math.cos(55*math.pi/180)):# and
        if  y >= -math.tan(55*math.pi/180) * (x-(48-20*math.cos(55*math.pi/180))) + 108+20*math.sin(55*math.pi/180):
            eq[2] = 1
        #if (x <= (y - (108+20*math.sin(55*math.pi/180) + 150*math.sin(35*math.pi/180)))/(-1)/math.tan(55*math.pi/180)+48-20*math.cos(55*math.pi/180)+ 150*math.sin(35*math.pi/180)):
        if y <= -math.tan(55*math.pi/180) * (x-(48 + 150*math.cos(35*math.pi/180)-20*math.cos(55*math.pi/180)))+ 108+20*math.sin(55*math.pi/180)+ 150*math.sin(35*math.pi/180):
            eq[3] = 1

        if 0 in eq:
            return False
        else:
            return True

    def ellipseSpace(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        #if x <= 2* abs(y-145)+246:# and y >= (x-246)/2 + 145:
        if ((x-246)**2)/(60**2)+((y-145)**2)/(30**2) - 1 <=0:
           return True
        else:
            return False 
    
    def enclosedSpace(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        eq = [0,0]
        #if x <= (y-63)/math.tan(45*math.pi/180) + 328:# and 
        if (x>= 328-60*math.cos(45*math.pi/180) and x<=328-60*math.cos(45*math.pi/180)+56*math.cos(45*math.pi/180) and
           y>=63 and y<=(63+60*math.sin(45*math.pi/180))+56*math.sin(45*math.pi/180)):
            if (x-(328-60*math.cos(45*math.pi/180)))*math.tan(45*math.pi/180)+(y-(63+60*math.sin(45*math.pi/180))) >=0:
                eq[0] = 1
            if (x-(328-60*math.cos(45*math.pi/180)))*math.tan(45*math.pi/180) - y + (63+60*math.sin(45*math.pi/180)) >=0:
                eq[1] = 1
        if (x>328-60*math.cos(45*math.pi/180)+56*math.cos(45*math.pi/180) and x <= 354 and y>=63 #-60*math.cos(45*math.pi/180)+56*math.tan(45*math.pi/180)
            and y<(63+60*math.sin(45*math.pi/180))+56*math.sin(45*math.pi/180)):
            if (x - (354- 27*math.cos(14.2956*math.pi/180)))*math.tan(14.2956) + (y - (138+27*math.sin(14.2956*math.pi/180))) <= 0:
                eq[0]= 1
        # if x>328 and x<=354 and y>=63 and y<=144.62519:
        #     if (x - (354- 27*math.cos(14.2956*math.pi/180)))*math.tan(14.2956) + (y - (138+27*math.sin(14.2956*math.pi/180))) <= 0:
        #         eq[0] = 1
            if y >= (x-328)*math.tan(45*math.pi/180)+63:
            #if (x-328)*math.tan(45*math.pi/180)-y-63<=0:
                eq[1] = 1  
        if (x > 354 and x <= 328 + 75*math.cos(45*math.pi/180) and y >= 63+26 and y<= 63+55 + 75*math.sin(45*math.pi/180)):  
            if y >= (x-328)*math.tan(45*math.pi/180)+63:
            #if (x-328)*math.tan(45*math.pi/180)-y-63<=0:
                eq[0] = 1
        #if (x >= (y - (63+60*math.sin(45)) * (-1)/math.tan(45*math.pi/180) + (328-60*math.cos(45)))):# and 
        #if y >= (x-(328-60*math.cos(45*math.pi/180)))*(-1)*math.tan(45*math.pi/180) + 63+60*math.sin(45*math.pi/180):
        
        #if (x >= (y - (63+60*math.sin(45)))/math.tan(45*math.pi/180) + (328-60*math.cos(45))):# and
        #if y <= (x-(328-60*math.cos(45*math.pi/180)))*math.tan(45*math.pi/180) + (63+60*math.sin(45*math.pi/180)):
        
            # if (x <= 328 + 75*math.cos(45*math.pi/180)) and (y>= 63 + 75*math.sin(45*math.pi/180)) and (y<= 63+55 + 75*math.sin(45*math.pi/180)):
            #     eq[1] = 1 
            #if #(x >= (y-138)*(75*math.cos(45*math.pi/180)-26)/(75*math.sin(45*math.pi/180)-20)+354):# and 
            #if y <= (x-354)*(75*math.sin(45*math.pi/180)-20)/(75*math.cos(45*math.pi/180)-26)+138:
            if (x-354)*(75*math.sin(45*math.pi/180)-20) - (y-138)*(75*math.cos(45*math.pi/180)-26) >= 0: 
                eq[1] = 1
        #if x >= (y-138)/math.tan(14.2956*math.pi/180)+354:
        #if y <= (x-354)*math.tan(14.2956*math.pi/180):
        #if y <= (x - (354- 27*math.cos(14.2956*math.pi/180)))*(-1)*math.tan(14.2956) + 138 + 27*math.sin(14.2956*math.pi/180):
                      #14.2956 is the computed angle of inclination for this segment
        
        if 0 in eq: #== [1,1,1,1,1,1]:
            return False
        else:
            return True
    
    def cShapeSpace(self, node):
        temp = [node[0], node[1]]
        x = temp[0]; y = temp[1]
        eq = [0,0,0]
        if x >= 210 and x<= 230 and y >= 230 and y <= 240:
            eq[0] = 1
        if x >= 200 and x<= 210 and y >= 230 and y <= 280:
            eq[1] = 1
        if x >= 210 and x<= 230 and y >= 270 and y <= 280:
            eq[2] = 1
        
        if 1 in eq:
            return True
        else:
            return False