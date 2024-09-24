import random
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """
    
    def generateMaze(self, maze: Maze3D):
        """
        Generate a 3D maze using Prim's algorithm.
        
        Parameters:
        maze (Maze3D): The maze object to be generated.
        """
        # Get the dimensions of the maze levels
        mazeDimensions = maze.m_levelDims
        numberOfLevels = len(mazeDimensions)
        
        # Initialize the maze with walls between all cells
        maze.initCells(addWallFlag=True)
        print("Initialized cells with walls.")
        
        # Choose a random starting cell within the maze
        startLevel = random.randint(0, numberOfLevels - 1)
        startRow = random.randint(0, mazeDimensions[startLevel][0] - 1)
        startColumn = random.randint(0, mazeDimensions[startLevel][1] - 1)
        startingCell = Coordinates3D(startLevel, startRow, startColumn)
        print(f"Starting cell: {startingCell}")
        
        # Initialize the frontier with the walls of the starting cell
        wallFrontier = []
        visitedCells = set()
        self.addWallsToFrontier(maze, startingCell, wallFrontier, visitedCells)
        print("Initialized frontier and visited set.")
        
        # Loop until there are no more walls in the frontier
        while wallFrontier:
            # Choose a random wall from the frontier
            currentWall = random.choice(wallFrontier)
            wallFrontier.remove(currentWall)
            cell1, cell2 = currentWall
            
            # If the second cell has already been visited, skip this wall
            if cell2 in visitedCells:
                continue
            
            # Remove the wall between cell1 and cell2
            maze.removeWall(cell1, cell2)
            visitedCells.add(cell2)
            
            # Add the walls of the new cell to the frontier
            self.addWallsToFrontier(maze, cell2, wallFrontier, visitedCells)
        
        self.m_mazeGenerated = True
        print("Maze generation complete.")
    
    def addWallsToFrontier(self, maze, cell, wallFrontier, visitedCells):
        """
        Add the walls of a cell to the frontier.
        
        Parameters:
        maze (Maze3D): The maze object.
        cell (Coordinates3D): The current cell.
        wallFrontier (list): The list of walls in the frontier.
        visitedCells (set): The set of visited cells.
        """
        visitedCells.add(cell)
        for neighbor in self.getNeighboringCells(maze, cell):
            if neighbor not in visitedCells:
                wallFrontier.append((cell, neighbor))

    def getNeighboringCells(self, maze, cell):
        """
        Get the neighboring cells of a given cell.
        
        Parameters:
        maze (Maze3D): The maze object.
        cell (Coordinates3D): The current cell.
        
        Returns:
        list: A list of neighboring cells.
        """
        # Define possible directions for neighboring cells
        directions = [
            Coordinates3D(0, 1, 0),  # up
            Coordinates3D(0, -1, 0),  # down
            Coordinates3D(0, 0, 1),  # right
            Coordinates3D(0, 0, -1),  # left
            Coordinates3D(1, 0, 0),  # above
            Coordinates3D(-1, 0, 0)  # below
        ]
        
        neighbors = []
        for direction in directions:
            neighbor = cell + direction
            # Check if the neighbor is within the maze boundaries and not a boundary itself
            if (0 <= neighbor.getLevel() < len(maze.m_levelDims)) and maze.checkCoordinates(neighbor) and not maze.isBoundary(neighbor):
                neighbors.append(neighbor)
        return neighbors
