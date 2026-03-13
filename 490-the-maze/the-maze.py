from typing import List

DIRS = [[0,1], [0,-1], [1,0], [-1,0]]

class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        if start[0] == destination[0] and start[1] == destination[1]:
            return True

        if startBlocked(maze, start[0], start[1]) or destBlocked(maze, destination[0], destination[1]):
            return False

        dir_queue = [[start, d] for d in DIRS]
        visited = [start]

        while len(dir_queue) > 0:
            move = dir_queue.pop(0)
            end_pos = getStopPoint(maze, move[0][0], move[0][1], move[1][0], move[1][1])

            if end_pos[0] == destination[0] and end_pos[1] == destination[1]:
                return True
            elif end_pos in visited:
                continue
            elif end_pos[0] != move[0][0] or end_pos[1] != move[0][1]:
                visited.append(end_pos)
                dir_queue += [[end_pos, d] for d in DIRS]
            else:
                continue

        return False

def getStopPoint(maze, r, c, dr, dc):
    # Get dimensions once
    rows, cols = len(maze), len(maze[0])
    
    # Roll while the next step is within bounds and is NOT a wall
    while 0 <= r + dr < rows and 0 <= c + dc < cols and maze[r + dr][c + dc] == 0:
        r += dr
        c += dc
        
    return [r, c]

def destBlocked(maze, r, c):
    return mazeAccess(maze, r + 1, c) + \
        mazeAccess(maze, r - 1, c) + \
        mazeAccess(maze, r, c + 1) + \
        mazeAccess(maze, r, c - 1) == 0

def startBlocked(maze, r, c):
    return mazeAccess(maze, r + 1, c) + \
        mazeAccess(maze, r - 1, c) + \
        mazeAccess(maze, r, c + 1) + \
        mazeAccess(maze, r, c - 1) == 4

def mazeAccess(maze, r, c):
    try:
        return maze[r][c]
    except IndexError:
        return 1
        

if __name__ == "__main__":
    solution = Solution()

    # Case 1: Successful Path
    maze1 = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0]
    ]
    start1 = [0, 4]
    dest1 = [4, 4]
    print(f"Case 1 (Expected: True): {solution.hasPath(maze1, start1, dest1)}")

    # Case 2: Impossible Stop
    maze2 = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0]
    ]
    start2 = [0, 4]
    dest2 = [3, 2]
    print(f"Case 2 (Expected: False): {solution.hasPath(maze2, start2, dest2)}")

    # Case 3: Trapped at Start
    maze3 = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]
    start3 = [1, 1]
    dest3 = [0, 0]
    print(f"Case 3 (Expected: False): {solution.hasPath(maze3, start3, dest3)}")

    # Case 4: Destination in a hallway (No wall to stop it)
    # The ball will pass [1, 2] but can only stop at [1, 1] or [1, 3]
    maze4 = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    start4 = [1, 1]
    dest4 = [1, 2]
    print(f"Case 4 (Expected: False): {solution.hasPath(maze4, start4, dest4)}")

    # Case 5: Maze with a Loop
    # The ball can go in circles; tests if your 'visited' set works
    maze5 = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0]
    ]
    start5 = [0, 0]
    dest5 = [4, 4]
    print(f"Case 5 (Expected: True): {solution.hasPath(maze5, start5, dest5)}")

    # Case 6: Dead End
    # Start is enclosed except for one way out that leads nowhere
    maze6 = [
        [0, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ]
    start6 = [0, 0]
    dest6 = [0, 1]
    print(f"Case 6 (Expected: True): {solution.hasPath(maze6, start6, dest6)}")

    # Case 7: Already at Destination
    # Tests if your code handles the start being the destination immediately
    maze7 = [[0, 0], [0, 0]]
    start7 = [0, 0]
    dest7 = [0, 0]
    print(f"Case 7 (Expected: True): {solution.hasPath(maze7, start7, dest7)}")