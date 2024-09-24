from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.solver_name = "wall"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        Solve the maze using the wall following algorithm.
        
        Parameters:
        maze (Maze3D): The 3D maze to be solved.
        entrance (Coordinates3D): The entrance coordinates of the maze.
        
        Returns:
        List[Coordinates3D]: The path from the entrance to the exit if found.
        """
        maze_completed = False
        explored_cells = set()
        position_stack = [entrance]
        direction_index = 0  # Start direction index
        move_directions = ['North', 'South', 'East', 'West', 'Up', 'Down']

        print(f"Starting at entrance: {entrance}")

        while position_stack:
            current_position = position_stack[-1]
            print("Currently at ", current_position)

            # Check if the current cell is an exit
            if current_position in maze.getExits():
                self.solved(entrance, current_position)
                maze_completed = True
                print("Exit found at ", current_position)
                self.solverPathAppend(current_position)
                break

            if current_position not in explored_cells:
                explored_cells.add(current_position)
                self.solverPathAppend(current_position, isBacktrack=False)

            move_found = False
            for i in range(len(move_directions)):
                new_direction_index = (direction_index + i) % len(move_directions)
                new_direction = move_directions[new_direction_index]
                next_position = self.getNextPosition(current_position, new_direction, maze)
                
                # Check if the next cell is an exit
                if next_position in maze.getExits():
                    self.solved(entrance, next_position)
                    maze_completed = True
                    print("Solved the maze! Exit found at ", next_position)
                    self.solverPathAppend(next_position)
                    break
                
                # Check if the move is valid
                if next_position and next_position not in explored_cells and not maze.hasWall(current_position, next_position):
                    position_stack.append(next_position)
                    direction_index = new_direction_index  # Update the facing direction
                    print("Moving from", current_position, "to", next_position, "towards", new_direction)
                    move_found = True
                    break
            
            if maze_completed:
                break
            
            if not move_found:
                # If no valid move is found, backtrack
                backtracked_position = position_stack.pop()
                print("No moves possible from", current_position, "backtracking to", backtracked_position)
                self.solverPathAppend(backtracked_position, isBacktrack=True)

        # Ensure the last step is outside the maze
        if current_position in maze.getExits():
            self.solved(entrance, current_position)
            self.solverPathAppend(current_position)

        return self.getSolverPath()

    def getNextPosition(self, position, direction, maze):
        """
        Get the next cell in the given direction from the current cell.
        
        Parameters:
        position (Coordinates3D): The current cell coordinates.
        direction (str): The direction to move ('North', 'South', 'East', 'West', 'Up', 'Down').
        maze (Maze3D): The maze object.
        
        Returns:
        Coordinates3D: The next cell coordinates if valid, otherwise None.
        """
        direction_deltas = {
            'North': (0, -1, 0),
            'South': (0, 1, 0),
            'East': (0, 0, 1),
            'West': (0, 0, -1),
            'Up': (1, 0, 0),  # Move up a level
            'Down': (-1, 0, 0)  # Move down a level
        }
        delta = direction_deltas[direction]
        next_position = Coordinates3D(position.getLevel() + delta[0], position.getRow() + delta[1], position.getCol() + delta[2])
        if self.isWithinBounds(next_position, maze):
            return next_position
        print(f"Cannot move {direction} from {position} to ({next_position.getLevel()}, {next_position.getRow()}, {next_position.getCol()}) - out of bounds or blocked")
        return None

    def isWithinBounds(self, cell, maze):
        """
        Check if the given cell is within the maze boundaries.
        
        Parameters:
        cell (Coordinates3D): The cell coordinates to check.
        maze (Maze3D): The maze object.
        
        Returns:
        bool: True if the cell is within bounds, False otherwise.
        """
        if cell in maze.getExits():
            return True

        return (0 <= cell.getLevel() < maze.levelNum() and
                0 <= cell.getRow() < maze.rowNum(cell.getLevel()) and
                0 <= cell.getCol() < maze.colNum(cell.getLevel()))
