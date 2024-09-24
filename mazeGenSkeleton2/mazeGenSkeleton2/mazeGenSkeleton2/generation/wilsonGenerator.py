from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from collections import defaultdict
from typing import List, Tuple
import random

class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson's algorithm maze generator.
    """

    def generateMaze(self, maze: Maze3D):
        """
        Generate a 3D maze using Wilson's algorithm.
        
        Parameters:
        maze (Maze3D): The maze object to be generated.
        """
        # Initialize the maze with walls between all cells
        maze.initCells(addWallFlag=True)

        # Dictionary to store cells and their neighbors
        cellNeighbors = defaultdict(list)
        totalCells = 0

        # Populate the cellNeighbors dictionary
        for level in range(maze.levelNum()):
            for row in range(maze.rowNum(level)):
                for col in range(maze.colNum(level)):
                    currentCell = Coordinates3D(level, row, col)
                    neighbors = [neighbor for neighbor in maze.neighbours(currentCell) if self.coordinateExists(neighbor, maze)]
                    if neighbors:
                        cellNeighbors[currentCell].extend(neighbors)
                    totalCells += 1

        # Randomly select the initial cell and add it to the maze
        initialCell = random.choice(list(cellNeighbors.keys()))
        maze.removeWall(initialCell, initialCell)
        visitedCells = {initialCell}
        
        # Loop until all cells are added to the maze
        while len(visitedCells) < totalCells:
            unvisitedCells = list(cellNeighbors.keys())
            # Choose a random unvisited cell and start a random walk until a visited cell is reached
            currentCell = random.choice(unvisitedCells)

            path = [currentCell]
            while currentCell not in visitedCells:
                nextCell = random.choice(cellNeighbors[currentCell])
                if nextCell in path:
                    loopIndex = path.index(nextCell)
                    path = path[:loopIndex + 1]
                else:
                    path.append(nextCell)
                currentCell = nextCell
            
            # Create the maze path by removing walls between cells in the path
            for i in range(len(path) - 1):
                maze.removeWall(path[i], path[i + 1])
                maze.removeWall(path[i + 1], path[i + 1])
                visitedCells.add(path[i])
                visitedCells.add(path[i + 1])

            # Remove visited cells from cellNeighbors
            cellNeighbors = {cell: neighbors for cell, neighbors in cellNeighbors.items() if cell not in visitedCells}

        self.m_mazeGenerated = True

    def coordinateExists(self, coord: Coordinates3D, maze: Maze3D) -> bool:
        """
        Check if the given coordinate exists within the maze boundaries.
        
        Parameters:
        coord (Coordinates3D): The coordinate to check.
        maze (Maze3D): The maze object.
        
        Returns:
        bool: True if the coordinate exists within the maze boundaries, False otherwise.
        """
        return (0 <= coord.getLevel() < maze.levelNum() and
                0 <= coord.getRow() < maze.rowNum(coord.getLevel()) and
                0 <= coord.getCol() < maze.colNum(coord.getLevel()))
