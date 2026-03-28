import heapq

# 1. The Heuristic: Calculates the "distance" to the goal
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    
    # Priority Queue: Stores (priority, current_position)
    # The agent always picks the lowest priority (F-score)
    frontier = []
    heapq.heappush(frontier, (0, start))
    
    # Memory: Tracking where we came from and the cost to get there
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        # Get the "best" next tile to explore
        current_f, current = heapq.heappop(frontier)

        # Success! Agent reached the goal
        if current == goal:
            break

        # Check neighbors (Up, Down, Left, Right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # Is the neighbor inside the maze and not a wall (1)?
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if maze[neighbor[0]][neighbor[1]] == 1:
                    continue
                
                new_cost = cost_so_far[current] + 1
                
                # If neighbor is new or we found a cheaper way to get there
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    if goal not in came_from: return None # No path found
    
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# --- TEST SETUP ---
# 0 = Path, 1 = Wall
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start_pos = (0, 0)
goal_pos = (4, 4)

path = a_star_search(maze, start_pos, goal_pos)

# Visualize the result
if path:
    print(f"Agent Path: {path}")
    for r in range(len(maze)):
        row_display = ""
        for c in range(len(maze[0])):
            if (r, c) == start_pos: row_display += " S "
            elif (r, c) == goal_pos: row_display += " G "
            elif (r, c) in path: row_display += " * "
            elif maze[r][c] == 1: row_display += " # "
            else: row_display += " . "
        print(row_display)
else:
    print("Agent could not find a path.")
