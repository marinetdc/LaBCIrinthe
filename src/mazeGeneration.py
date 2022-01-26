### Adapted from https://github.com/Minifranger/mini_maze_bot

import numpy
import random
import time


# 0 is free cells, 1 is wall cells and 0.5 is visited cells
### reversed in exportToCsv in order to be compatible with main code
class Maze:
    # width and height are in cells.
    def __init__(self, levelName, width=20, height=20):
        self.levelName = levelName
        self.width = width
        self.height = height
        self.cells = numpy.ones((self.height, self.width))
        self.dfs()
        #self.exportToCsv()

    def change_cell(self, cell, value):
        self.cells[cell] = value

    # x is the matrix column index
    # y is the matrix row index
    # so matrix index are cell = (y, x)
    # pygame draw x from left to right and y from top to bottom

    #################################################################################################################
    #                                               DFS GENERATION                                                  #
    #################################################################################################################

    def unvisited_cell_neighbors(self, cell):
        neighbors = []
        west = []
        north = []
        east = []
        south = []
        if cell[1] > 1 and self.cells[cell[0], cell[1] - 2] == 1:
            west.extend([(cell[0], cell[1] - 1), (cell[0], cell[1] - 2)])
        if cell[1] < self.width - 2 and self.cells[cell[0], cell[1] + 2] == 1:
            east.extend([(cell[0], cell[1] + 1), (cell[0], cell[1] + 2)])
        if cell[0] > 1 and self.cells[cell[0] - 2, cell[1]] == 1:
            north.extend([(cell[0] - 1, cell[1]), (cell[0] - 2, cell[1])])
        if cell[0] < self.height - 2 and self.cells[cell[0] + 2, cell[1]] == 1:
            south.extend([(cell[0] + 1, cell[1]), (cell[0] + 2, cell[1])])
        neighbors.extend([west, north, east, south])
        neighbors = [x for x in neighbors if x != []]
        return neighbors

    # If wall is a cell, then do step of 2
    # Credit to https://github.com/The-Ofek-Foundation/Maze
    def dfs(self):
        visited = []
        current_cell = (0, 0)
        visited.append(current_cell)
        self.change_cell(current_cell, 0)
        start = 0
        
        while visited:
            neighbors = self.unvisited_cell_neighbors(current_cell)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.change_cell(next_cell[0], 0)
                self.change_cell(next_cell[1], 0)
                visited.extend([next_cell[0], next_cell[1]])
                current_cell = next_cell[1]
            else:
                if len(visited) > 1:
                    self.change_cell(visited[-1], 0.5)
                    if start == 0:
                        self.change_cell(visited[-1], 3)
                        start += 1
                    del visited[-1]
                    self.change_cell(visited[-1], 0.5)
                    del visited[-1]
                    current_cell = visited[-1]
                else:
                    self.change_cell(visited[-1], 2)
                    current_cell = visited[-1]
                    del visited[-1]

    def exportToCsv(self):
        ### reverse dictionnary in order to be compatible with main code
        for i in range(self.width):
                for j in range(self.height):
                        if(self.cells[i,j] == 1):
                                self.cells[i,j] = 0
                        elif(self.cells[i,j] == 0.5):
                                self.cells[i,j] = 1
        numpy.savetxt('./assets/levels/' + self.levelName + '.csv', self.cells, delimiter=',', fmt = '%1d')
        return None

#X = Maze(levelName = 'teeest')
