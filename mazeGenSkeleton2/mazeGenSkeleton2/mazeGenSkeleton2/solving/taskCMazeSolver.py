from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from collections import deque

class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation. You'll need to complete its implementation for task C.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMaze(self, maze: Maze3D, entry_point: Coordinates3D = None):
        # We call the solve maze without the entrance for task C
        self.solveMazeTaskC(maze)

    def solveMazeTaskC(self, maze: Maze3D):
        """
        Solve the maze, used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        find the entrance and exit pair (see project specs for requirements of this task).
        """
        entry_points = maze.getEntrances()
        exit_points = maze.getExits()

        if not entry_points:
            print("No entry points found in the maze.")
            return

        if not exit_points:
            print("No exit points found in the maze.")
            return

        print(f"Entry points: {entry_points}")
        print(f"Exit points: {exit_points}")

        # Initialize variables for the best path and cost
        optimal_path = None
        optimal_cost = float('inf')
        optimal_entry = None
        optimal_exit = None

        # Explore from each entry point to find all exit points and paths
        for entry in entry_points:
            bfs_queue = deque([(entry, [entry], 0)])
            visited_nodes = set([entry])
            local_optimal_cost = float('inf')
            local_optimal_path = None
            local_optimal_exit = None

            print(f"Exploring from entry point: {entry}")

            while bfs_queue:
                current_node, path, explored_cells = bfs_queue.popleft()
                self.solverPathAppend(current_node)  # Record each step

                if current_node in exit_points:
                    current_cost = explored_cells + len(path)
                    if current_cost < local_optimal_cost:
                        local_optimal_cost = current_cost
                        local_optimal_path = path
                        local_optimal_exit = current_node
                        print(f"New local optimal path found from {entry} to {current_node} with cost {local_optimal_cost}")

                for neighbor in self.get_neighbors(maze, current_node):
                    if neighbor not in visited_nodes and not maze.hasWall(current_node, neighbor):
                        visited_nodes.add(neighbor)
                        bfs_queue.append((neighbor, path + [neighbor], explored_cells + 1))

            # Update the global optimal path if the local optimal is better
            if local_optimal_path and local_optimal_cost < optimal_cost:
                optimal_cost = local_optimal_cost
                optimal_path = local_optimal_path
                optimal_entry = entry
                optimal_exit = local_optimal_exit
                print(f"New global optimal path found from {optimal_entry} to {optimal_exit} with cost {optimal_cost}")

        if optimal_path:
            self.solved(optimal_entry, optimal_exit)
            for cell in optimal_path:
                self.solverPathAppend(cell)
            print(f"Optimal path found from {optimal_entry} to {optimal_exit}")
        else:
            print("No path found.")

    def get_neighbors(self, maze, current_position):
        level = current_position.getLevel()
        row = current_position.getRow()
        col = current_position.getCol()
        neighbors = []
        directions = [(0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]

        for direction in directions:
            neighbor = Coordinates3D(level + direction[0], row + direction[1], col + direction[2])
            if self.is_within_bounds(neighbor, maze):
                if maze.checkCoordinates(neighbor):
                    neighbors.append(neighbor)
        return neighbors

    def is_within_bounds(self, cell, maze):
        if 0 <= cell.getLevel() < len(maze.m_levelDims) and \
           0 <= cell.getRow() < maze.m_levelDims[cell.getLevel()][0] and \
           0 <= cell.getCol() < maze.m_levelDims[cell.getLevel()][1]:
            return True
        return False
