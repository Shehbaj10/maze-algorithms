# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Implementation of Task D maze generator.
#
# author = 'Jeffrey Chan'
# copyright = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from random import randint, choice
from collections import deque
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

class TaskDMazeGenerator(MazeGenerator):
    """
    Task D maze generator. This class generates a maze specifically tailored
    to challenge different maze solvers based on their solving algorithms.
    """

    def generateMaze(self, maze_structure: Maze3D, solver_identity: str = None):
        """
        Generate a maze based on the solver's characteristics if known.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        - solver_identity (str): The name of the solver for which the maze is being generated.
        """
        print(f"Generating maze for solver: {solver_identity if solver_identity else 'Unknown/Mystery Solver'}")
        
        # Generate maze based on the solver's known characteristics
        if solver_identity == 'wallFollower':
            self.generate_for_wall_follower(maze_structure)
        elif solver_identity == 'pledgeSolver':
            self.generate_for_pledge_solver(maze_structure)
        else:
            self.generate_complex_maze(maze_structure)  # Default for mystery or unspecified solver

        # Mark the maze as generated
        self.m_mazeGenerated = True

    def generate_for_wall_follower(self, maze_structure):
        """
        Generate a maze with loops and dead-ends to challenge wall-following solvers.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        """
        self.generate_maze_with_loops_and_dead_ends(maze_structure)

    def generate_for_pledge_solver(self, maze_structure):
        """
        Generate a maze with frequent turns and junctions to challenge the Pledge algorithm.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        """
        self.generate_maze_with_frequent_turns(maze_structure)

    def generate_complex_maze(self, maze_structure):
        """
        Generate a highly complex and unpredictable maze to challenge any solver.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        """
        self.generate_maze_with_mixed_features(maze_structure)

    def generate_maze_with_loops_and_dead_ends(self, maze_structure):
        """
        Generate a maze with loops and dead-ends.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        """
        maze_structure.initCells(True)  # Initialize the maze cells with walls
        all_positions = [Coordinates3D(lvl, rw, cl)
                         for lvl in range(maze_structure.levelNum())
                         for rw in range(maze_structure.rowNum(lvl))
                         for cl in range(maze_structure.colNum(lvl))]
        initial_position = choice(all_positions)  # Choose a random starting position
        visited_positions = set([initial_position])  # Keep track of visited positions
        position_stack = [initial_position]  # Stack for DFS

        # Depth-First Search (DFS) to create maze with loops and dead-ends
        while position_stack:
            current_position = position_stack.pop()
            # Get unvisited neighbors that have walls
            neighbors = [neighbor for neighbor in maze_structure.neighbours(current_position) 
                         if maze_structure.hasWall(current_position, neighbor) and neighbor not in visited_positions]
            if neighbors:
                position_stack.append(current_position)  # Put current back to stack for further exploration
                chosen_neighbor = choice(neighbors)  # Choose a random neighbor
                maze_structure.removeWall(current_position, chosen_neighbor)  # Remove the wall between current and chosen neighbor
                visited_positions.add(chosen_neighbor)  # Mark the chosen neighbor as visited
                position_stack.append(chosen_neighbor)  # Add the chosen neighbor to the stack

    def generate_maze_with_frequent_turns(self, maze_structure):
        """
        Generate a maze with frequent turns and junctions.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        """
        maze_structure.initCells(True)  # Initialize the maze cells with walls
        initial_position = Coordinates3D(0, 0, 0)  # Fixed start point for predictable pattern creation
        position_stack = [initial_position]  # Stack for DFS
        visited_positions = set([initial_position])  # Keep track of visited positions

        # Depth-First Search (DFS) to create maze with frequent turns
        while position_stack:
            current_position = position_stack.pop()
            # Get unvisited neighbors that don't have walls
            neighbors = [neighbor for neighbor in maze_structure.neighbours(current_position) 
                         if not maze_structure.hasWall(current_position, neighbor) and neighbor not in visited_positions]
            if neighbors:
                chosen_neighbor = choice(neighbors)  # Choose a random neighbor
                maze_structure.removeWall(current_position, chosen_neighbor)  # Remove the wall between current and chosen neighbor
                visited_positions.add(chosen_neighbor)  # Mark the chosen neighbor as visited
                position_stack.append(chosen_neighbor)  # Add the chosen neighbor to the stack

    def generate_maze_with_mixed_features(self, maze_structure):
        """
        Generate a complex maze with mixed features.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure to be generated.
        """
        maze_structure.initCells(True)  # Initialize the maze cells with walls
        # Choose a random starting position
        initial_position = Coordinates3D(randint(0, maze_structure.levelNum() - 1), 
                                         randint(0, maze_structure.rowNum(0) - 1), 
                                         randint(0, maze_structure.colNum(0) - 1))
        visited_positions = set([initial_position])  # Keep track of visited positions
        frontier_positions = [initial_position]  # List for BFS

        # Breadth-First Search (BFS) to create a complex maze with mixed features
        while frontier_positions:
            current_position = frontier_positions.pop(0)
            neighbors = maze_structure.neighbours(current_position)
            for neighbor in neighbors:
                if neighbor not in visited_positions and self.checkCoordinates(maze_structure, neighbor):
                    maze_structure.removeWall(current_position, neighbor)  # Remove the wall between current and neighbor
                    visited_positions.add(neighbor)  # Mark the neighbor as visited
                    frontier_positions.append(neighbor)  # Add the neighbor to the frontier

    def checkCoordinates(self, maze_structure, coord: Coordinates3D) -> bool:
        """
        Check if the coordinates are within the maze boundaries.
        
        Parameters:
        - maze_structure (Maze3D): The 3D maze structure.
        - coord (Coordinates3D): The coordinates to check.
        
        Returns:
        - bool: True if the coordinates are within the boundaries, False otherwise.
        """
        level, row, col = coord.getLevel(), coord.getRow(), coord.getCol()
        if not (0 <= level < maze_structure.levelNum()):
            return False
        rowNum, colNum = maze_structure.rowNum(level), maze_structure.colNum(level)
        return 0 <= row < rowNum and 0 <= col < colNum
