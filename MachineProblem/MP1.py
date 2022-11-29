import random
import copy

class Coordinate(object):
    def __init__(self,row,col):
        self._row = row
        self._col = col
    def __str__(self):
        return "<" + str(self._row) + "," + str(self._col) + ">"
    def getRow(self):
        return self._row
    def getCol(self):
        return self._col


class Grid(object):
    def __init__(self,rows,cols,K):
        self._rows = rows
        self._cols = cols
        self._K = K
        self._gridList = []
        self.createGrid()
    def createGrid(self):
        for row in range(self._rows):
            self._temp = []
            for col in range(self._cols):
                self._temp.append(random.randint(0,self._K-1))
            self._gridList.append(self._temp[:])
        # self._gridList = [[0,2,1,0,2,2],[0,0,1,0,0,0],[1,1,0,2,2,2],[1,0,2,0,2,2],[2,0,1,0,1,1]]
    def printGrid(self):
        for row in range(len(self._gridList)):
            for col in range(len(self._gridList[0])):
                print("[" + str(self._gridList[row][col]) + "]", end = " ")
            print("")
    def __str__(self):
        self._str = ""
        for row in range(len(self._gridList)):
            for col in range(len(self._gridList[0])):
                self._str = self._str + "[" + str(self._gridList[row][col]) + "]"
            self._str = self._str + '\n'
        return self._str
    def getRows(self):
        return len(self._gridList)
        #return self._rows
    def getCols(self):
        return len(self._gridList[0])
        #return self._cols
    def getGrid(self):
        return self._gridList.copy()


class Game(object):
    def __init__(self,rows,cols,K):
        self._grid = Grid(rows,cols,K)
        self._play = True
        self._neighbors = 0
        self._score = 0
        self._initTargetList()
    def __str__(self):
        return self._grid.__str__()
    def _set_neighbors(self,neighbors):
        self._neighbors = neighbors
    def _findNeighbors(self,grid,target,coordinate):
        # print("enter")
        if target == grid[coordinate.getRow()][coordinate.getCol()]:
            grid[coordinate.getRow()][coordinate.getCol()] = -1
            self._neighbors += 1
            # top
            if coordinate.getRow() >= 1:
                self._findNeighbors(grid,target,Coordinate(coordinate.getRow()-1,coordinate.getCol()))
            # bottom
            if coordinate.getRow()+1 < self._grid.getRows():
                self._findNeighbors(grid,target,Coordinate(coordinate.getRow()+1,coordinate.getCol()))
            # left
            if coordinate.getCol() >= 1:
                self._findNeighbors(grid,target,Coordinate(coordinate.getRow(),coordinate.getCol()-1))
            # right
            if coordinate.getCol()+1 < self._grid.getCols():
                self._findNeighbors(grid,target,Coordinate(coordinate.getRow(),coordinate.getCol()+1))
        return self._neighbors

    def _updateGrid(self,grid,to_print=True):
        gridCopy = copy.deepcopy(grid[:])
        for row, sublist in enumerate(gridCopy):
            for col, item in enumerate(sublist):
                if item==-1:
                    row_copy = row
                    grid[row_copy][col] = ' '
                    while row_copy>=1:
                        grid[row_copy][col] = grid[row_copy-1][col]
                        grid[row_copy-1][col] = ' '
                        row_copy -=1
        # check if column is entirely ' '
        for row, sublist in enumerate(grid):
            for col, item in enumerate(sublist):
                temp = [sublist[col]for sublist in grid]
                if all(item==' ' for item in temp):
                    for r in range(len(grid)):
                        del(grid[r][col])
        if to_print==True:            
            print(self._grid)
    
    def _initTargetList(self):
        self._dictionary = {}
        grid = self._grid.getGrid()
        for row, sublist in enumerate(grid):
            for col, item in enumerate(sublist):
                if not item in self._dictionary:
                    self._dictionary[item] = []
        self._findAllNeighbors()

    def _findAllNeighbors(self):
        grid_check = copy.deepcopy(self._grid.getGrid())
        for x in range(len(grid_check)):
            for y in range(len(grid_check[len(grid_check)-1])):
                target = grid_check[x][y]
                if not target == -1:
                    self._set_neighbors(0)
                    num_neighbors = self._findNeighbors(grid_check,grid_check[x][y],Coordinate(x,y))
                    if num_neighbors > 2:
                        self._dictionary[target].append(num_neighbors)
        
    def _isEmptyDictionary(self):
        for key in self._dictionary.keys():
            if not key == ' ':
                if not self._dictionary[key]==[]:
                    return False
        return True
    
    def play(self,coordinate=None):
        self._play = not self._isEmptyDictionary()#False
        
        if not coordinate == None and self._play == True:
            grid_check = copy.deepcopy(self._grid.getGrid())
            grid = self._grid.getGrid()
            self._set_neighbors(0)
            
            # check if coordinate is out of bounds
            if coordinate.getRow()<0 or coordinate.getRow()>= len(grid_check) or \
                coordinate.getCol()<0 or coordinate.getCol()>=len(grid_check[len(grid_check)-1]):
                print("The input coordinate is out of bonds. Please input row:<0,"+str(len(grid_check)-1)+"> and col:<0,"+ \
                        str(len(grid_check[len(grid_check)-1])-1)+">")
                self._play = True
                return self._play

            # check if the adjacent cell and the block are less than or equal to 2
            target = grid_check[coordinate.getRow()][coordinate.getCol()]
            if self._dictionary[target]==[] and self._isEmptyDictionary==False:
                print("The adjacent cell blocks are of size less than or equal to 2")
                self.play = True
                return self._play
            
            found_neighbors = self._findNeighbors(grid,target,coordinate)
            self._updateGrid(grid)
            self._updateGrid(grid_check,False)
            self._initTargetList()
            self._score += (found_neighbors-2)**2
            print("score: "+str(self._score))
            self._dictionary[target].remove(found_neighbors)

        return self._play


def main():
    [rows,cols,K] = map(int,input("Enter M, N, and K, separated by spaces: ").split(' '))
    matching_game = Game(rows,cols,K)
    
    print(matching_game)
    cont = matching_game.play() 
    while cont:
        try:
            (row,column) = map(int,input("Enter row and column: ").split(' '))
            coordinate  = Coordinate(row,column)
            print(coordinate)
            cont = matching_game.play(coordinate)
        except:
            cont = matching_game.play()

if __name__=="__main__":
    main()