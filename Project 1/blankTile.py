import numpy as np

class blankTile:

    # def __init__(self):

    #     self.matrix = []

    def getLocation(self, matrix):
        res = np.where(matrix == 0) #Stores location of the zeroth cell in the matrix
        i = res[0][0]
        j = res[1][0]
        zCell = [i, j]

        return zCell

    def moveLeft(self, matrix, x, y):
        if y > 0:
            temp = matrix[x][y]
            node = []#matrix
            for ind in range(len(matrix)):
                node.append([])
                for col in range(len(matrix[ind])):
                    node[ind].append(matrix[ind][col])
            node[x][y] = matrix[x][y-1]
            node[x][y-1] = temp
            node = np.array(node)
            if node[x][y] != temp:
                return node
            else:
                return [""]
        else:
            return [""]

    def moveRight(self, matrix, x, y):
        if y < 3:
            temp = matrix[x][y]
            node = []#matrix
            for ind in range(len(matrix)):
                node.append([])
                for col in range(len(matrix[ind])):
                    node[ind].append(matrix[ind][col])
            node[x][y] = matrix[x][y+1]
            node[x][y+1] = temp
            node = np.array(node)
            if node[x][y] != temp:
                return node
            else:
                return [""]
            #print(self.matrix)
        else:
            return [""]

    def moveUp(self, matrix, x, y):
        if x > 0:
            temp = matrix[x][y]
            node = []#matrix
            for ind in range(len(matrix)):
                node.append([])
                for col in range(len(matrix[ind])):
                    node[ind].append(matrix[ind][col])
            node[x][y] = matrix[x-1][y]
            node[x-1][y] = temp
            node = np.array(node)
            if node[x][y] != temp:
                return node
            else:
                return [""] 
            #print(self.matrix)
        else:
            return [""]

    def moveDown(self, matrix, x, y):
        if x < 3:
            temp = matrix[x][y]
            node = []#matrix
            for ind in range(len(matrix)):
                node.append([])
                for col in range(len(matrix[ind])):
                    node[ind].append(matrix[ind][col])
            node[x][y] = matrix[x+1][y]
            node[x+1][y] = temp
            node = np.array(node)
            if node[x][y] != temp:
                return node
            else:
                return [""]
        else:
            return [""]