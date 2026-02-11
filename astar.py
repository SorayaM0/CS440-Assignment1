
# TODO (Part 1):
# Implement basic A* search with Manhattan heuristic

# implementing heapq for now 
# option to write our own as detailed in project description
# we can do that if we have time
import heapq 

class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g # cost from start
        self.h = h # heuristic
        self.f = g + h # cost + heuristic
        self.parent = parent # parent (previous) node

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def get_neighbors(gridworld, row, col):
    neighbors = []
    # simulate down, up, right, and left with coordinates
    for dir_row, dir_col in [(1,0), (-1,0), (0,1), (0,-1)]:
        new_row, new_col = row + dir_row, col + dir_col
        if 0 <= new_row < gridworld.rows and 0 <= new_col < gridworld.cols:
            # check if cell is not blocked 
            if gridworld.grid[new_row][new_col] != '#':
                # if not blocked append
                neighbors.append((new_row, new_col))
            # else, implied to move on
    return neighbors

def astar(gridworld, start, goal):
    open_list = [] # A* maintains an open list
    closed_list = set()

    # Create starting node using Manhattan heuristic
    first_node = Node(start, g=0, h=manhattan_distance(start,goal))
    heapq.heappush(open_list, first_node)

    g_value = {start: 0}

    while open_list:
        # pop current node from heap
        current = heapq.heappop(open_list)

        if current.position == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        # Used closed list to help store items
        closed_list.add(current.position)

        for neighbor in get_neighbors(gridworld, *current.position):
            if neighbor in closed_list:
                continue

            tentative_g = current.g + 1

            if neighbor not in g_value or tentative_g < g_value[neighbor]:
                g_value[neighbor] = tentative_g
                h = manhattan_distance(neighbor, goal)
                neighbor_node = Node(neighbor, tentative_g, h, current)
                heapq.heappush(open_list, neighbor_node)
