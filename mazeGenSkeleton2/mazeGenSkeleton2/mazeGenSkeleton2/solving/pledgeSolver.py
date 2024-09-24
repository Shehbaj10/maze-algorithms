from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class PledgeMazeSolver(MazeSolver):
    def __init__(self):
        super().__init__()
        self.solver_name = "pledge"

    def solveMaze(self, maze: Maze3D, start: Coordinates3D):
        """
        Solve the maze using Pledge algorithm.
        
        Parameters:
        maze (Maze3D): The 3D maze to be solved.
        start (Coordinates3D): The entrance coordinates of the maze.
        
        Returns:
        List[Coordinates3D]: The path from the entrance to the exit if found.
        """
        move_directions = [(0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        current_dir = 0  # Start direction
        current_pos = start
        visited = set()
        self.resetPathAndCellExplored()  # Reset the solver path and cell exploration count
        self.solverPathAppend(current_pos)
        path_stack = [(current_pos, current_dir)]
        steps = 0
        max_steps = 1000  # Limit the number of steps to prevent infinite loops

        while path_stack and steps < max_steps:
            current_pos, current_dir = path_stack[-1]

            # Check if the current position is an exit
            if current_pos in maze.m_exit:
                self.solved(start, current_pos)
                break

            # Try to move in the current direction
            next_pos = self.calculateNextPosition(current_pos, move_directions[current_dir])
            if self.isValidMove(maze, current_pos, next_pos) and next_pos not in visited:
                current_pos = next_pos
                visited.add(current_pos)
                self.solverPathAppend(current_pos)
                path_stack.append((current_pos, current_dir))
                steps += 1
            else:
                # If move is invalid, try to turn and find a valid move
                found_move = False
                for i in range(1, 6):  # Try all six possible directions
                    new_dir = (current_dir + i) % 6
                    next_pos = self.calculateNextPosition(current_pos, move_directions[new_dir])
                    if self.isValidMove(maze, current_pos, next_pos) and next_pos not in visited:
                        current_dir = new_dir
                        current_pos = next_pos
                        visited.add(current_pos)
                        self.solverPathAppend(current_pos)
                        path_stack.append((current_pos, current_dir))
                        found_move = True
                        steps += 1
                        break

                # If no valid move is found, backtrack
                if not found_move:
                    path_stack.pop()
                    if path_stack:
                        current_pos, current_dir = path_stack[-1]
                        self.solverPathAppend(current_pos, isBacktrack=True)
                    steps += 1

            # Additional check for exits adjacent to the current position
            for dir in move_directions:
                next_pos = self.calculateNextPosition(current_pos, dir)
                if next_pos in maze.m_exit:
                    self.solved(start, next_pos)
                    path_stack.append((next_pos, current_dir))
                    self.solverPathAppend(next_pos)
                    break

        if current_pos in maze.m_exit:
            self.solved(start, current_pos)

        return self.getSolverPath()

    def calculateNextPosition(self, position, direction):
        """
        Calculate the next position based on the current position and direction.
        
        Parameters:
        position (Coordinates3D): The current coordinates.
        direction (tuple): The direction to move (level, row, col).
        
        Returns:
        Coordinates3D: The next coordinates.
        """
        return Coordinates3D(
            position.getLevel() + direction[0],
            position.getRow() + direction[1],
            position.getCol() + direction[2]
        )

    def isValidMove(self, maze, current, next):
        """
        Check if the move from current to next is valid.
        
        Parameters:
        maze (Maze3D): The maze object.
        current (Coordinates3D): The current coordinates.
        next (Coordinates3D): The next coordinates.
        
        Returns:
        bool: True if the move is valid, False otherwise.
        """
        level_dims = maze.m_levelDims
        # Check if the next position is within maze boundaries
        if not (0 <= next.getLevel() < len(level_dims) and
                0 <= next.getRow() < level_dims[next.getLevel()][0] and
                0 <= next.getCol() < level_dims[next.getLevel()][1]):
            return False
        # Check if the coordinates are valid within the maze
        if not maze.checkCoordinates(next):
            return False
        # Check if there's no wall between current and next
        for neighbor, has_wall in maze.m_graph.m_vertListMap.get(current, []):
            if neighbor == next and not has_wall:
                return True
        return False
