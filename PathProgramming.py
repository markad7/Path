from queue import Queue, PriorityQueue
import time

def read_map_data(file_name):
    with open(file_name) as f:
        return [l.strip() for l in f.readlines() if len(l) > 1]

def bfs_search(map_data, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    iterations = 0

    while not frontier.empty():
        current = frontier.get()
        iterations += 1
        if current == goal:
            break
        for next in neighbors(current, map_data):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    path = construct_path(start, goal, came_from)
    return path, iterations

def greedy_search(map_data, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    came_from[start] = None
    iterations = 0

    while not frontier.empty():
        _, current = frontier.get()
        iterations += 1
        if current == goal:
            break
        for next in neighbors(current, map_data):
            if next not in came_from:
                priority = heuristic(next, goal)
                frontier.put((priority, next))
                came_from[next] = current

    path = construct_path(start, goal, came_from)
    return path, iterations

def a_star_search(map_data, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    iterations = 0

    while not frontier.empty():
        _, current = frontier.get()
        iterations += 1
        if current == goal:
            break
        for next in neighbors(current, map_data):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put((priority, next))
                came_from[next] = current

    path = construct_path(start, goal, came_from)
    return path, iterations

def neighbors(cell, map_data):
    row, col = cell
    rows = len(map_data)
    cols = len(map_data[0])
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    result = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols and map_data[new_row][new_col] != '*':
            result.append((new_row, new_col))
    return result

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def construct_path(start, goal, came_from):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def test_algorithms_on_maps():
    map_files = ["cave300x300", "cave600x600", "cave900x900"]
    start_coords = [(2, 2), (2, 2), (2, 2)]
    goal_coords = [(295, 257), (598, 595), (898, 895)]

    algorithms = {"BFS": bfs_search, "Greedy": greedy_search, "A*": a_star_search}

    for file_name, start, goal in zip(map_files, start_coords, goal_coords):
        map_data = read_map_data(file_name)
        print("\nTesting algorithms on map:", file_name)
        for algorithm_name, algorithm in algorithms.items():
            start_time = time.time()
            path, iterations = algorithm(map_data, start, goal)
            end_time = time.time()
            if path:
                print(f"{algorithm_name} Path found in {end_time - start_time:.5f} seconds")
                print(f"{algorithm_name} Path length: {len(path) - 1}")
                print(f"{algorithm_name} Iterations: {iterations}")
            else:
                print(f"{algorithm_name} No path found")

test_algorithms_on_maps()
