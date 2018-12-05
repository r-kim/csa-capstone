from random import randrange
from heapq import heappop, heappush
from math import inf

directions = ["U", "D", "L", "R"]

def new_position_after_move(i, j, move):
    explore_i = i
    explore_j = j
    if move == "U":
      explore_i = i - 1
    elif move == "D":
      explore_i = i + 1
    elif move == "L":
      explore_j = j - 1
    elif move == "R":
      explore_j = j + 1
    return explore_i, explore_j

def bfs(grid, start_i, start_j, swags):
  grid_copy = [row[:] for row in grid]
  bfs_queue = [[start_i, start_j]]
  paths_and_swags = []
  for i in range(len(grid)):
      row = []
      for j in range(len(grid[0])):
          row.append([[ "(" + str(i) + "," + str(j) + ")"], []])
      paths_and_swags.append(row)

  count = 0;
  while bfs_queue:
    i,j = bfs_queue.pop(0)
    grid_copy[i][j] = "visited"
    for direction in directions:
      explore_i, explore_j = new_position_after_move(i, j, direction)

      if is_out_of_grid(grid, explore_i, explore_j):
         continue
      elif is_this_cell_available(grid, grid_copy, explore_i, explore_j):
        new_paths = paths_and_swags[i][j][0] + [ "(" + str(explore_i) + "," + str(explore_j) + ")" ]
        new_swags = paths_and_swags[i][j][1]

        if grid[explore_i][explore_j] in swags:
          item = grid[explore_i][explore_j]
          new_swags = paths_and_swags[i][j][1] + [ str(item)]

        paths_and_swags[explore_i][explore_j][0] = new_paths
        paths_and_swags[explore_i][explore_j][1] = new_swags
        bfs_queue.append([explore_i, explore_j])
        count += 1

  grid[i][j] = "end"
  return paths_and_swags, count

def dijkstras( grid, start_i, start_j):
  grid_copy = [row[:] for row in grid]
  paths_and_distances = []
  for i in range(len(grid)):
      row = []
      for j in range(len(grid[0])):
          row.append([inf, [ "(" + str(i) + "," + str(j) + ")"]])
      paths_and_distances.append(row)
  paths_and_distances[start_i][start_j][0] = 0
  vertices_to_explore = [(0, start_i, start_j)]
  count = 0;

  while vertices_to_explore:
    current_distance, current_i, current_j = heappop(vertices_to_explore)
    grid_copy[current_i][current_j] = "visited"
    for direction in directions:
      explore_i, explore_j = new_position_after_move(current_i, current_j, direction)
      new_distance = current_distance + 1
      new_path = paths_and_distances[current_i][current_j][1] + [ "(" + str(explore_i) + "," + str(explore_j) + ")" ]

      if is_out_of_grid(grid, explore_i, explore_j):
         continue
      elif is_this_cell_available(grid, grid_copy, explore_i, explore_j) and new_distance < paths_and_distances[explore_i][explore_j][0]:
         paths_and_distances[explore_i][explore_j][0] = new_distance
         paths_and_distances[explore_i][explore_j][1] = new_path
         heappush(vertices_to_explore, (new_distance, explore_i, explore_j))
         count += 1

  return paths_and_distances, count

def is_out_of_grid(grid, explore_i, explore_j):
    return explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0])

def is_this_cell_available(grid, grid_copy, explore_i, explore_j):
    return grid[explore_i][explore_j] != "wall" and grid_copy[explore_i][explore_j] != "visited"


# using Manhattan Distance since it's 2D grid and only moves in 4 directions; No diagnoal movement
def heuristic(explore_i, explore_j, target_i, target_j):
  x_distance = abs(explore_i - target_i)
  y_distance = abs(explore_j - target_j)
  return x_distance + y_distance

def a_star(grid, start_i, start_j, end_i, end_j):
  grid_copy = [row[:] for row in grid]
  #list that has 3 type of data in it; distance, path and swag
  distances_paths_and_swags = []
  #initialize grid setting all the cells with infinite distance
  for i in range(len(grid)):
      row = []
      for j in range(len(grid[0])):
          row.append([inf, [ "(" + str(i) + "," + str(j) + ")"], [""]])
      distances_paths_and_swags.append(row)
  # set the start cell's distance to zero
  distances_paths_and_swags[start_i][start_j][0] = 0
  # set the vertices_to_explore list with the start cell
  vertices_to_explore = [(0, start_i, start_j)]
  count = 0;
  # iterate til vertices_to_explore has a vertice to explore and didn't reach the end cell yet
  while vertices_to_explore and distances_paths_and_swags[end_i][end_j][0] == inf:
    current_distance, current_i, current_j = heappop(vertices_to_explore)
    grid_copy[current_i][current_j] = "visited"
    for direction in directions:
      explore_i, explore_j = new_position_after_move(current_i, current_j, direction)

      new_distance = current_distance + 1 + heuristic(explore_i, explore_j, end_i, end_j)
      new_path = distances_paths_and_swags[current_i][current_j][1] + [ "(" + str(explore_i) + "," + str(explore_j) + ")" ]
      #if explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0]):
      if is_out_of_grid(grid, explore_i, explore_j):
         continue
      elif is_this_cell_available(grid, grid_copy, explore_i, explore_j) \
           and new_distance < distances_paths_and_swags[explore_i][explore_j][0]:
         item_in_next_cell = ""
         if (grid[explore_i][explore_j] != "empty"):
           item_in_next_cell = grid[explore_i][explore_j][0]
         new_swag = distances_paths_and_swags[current_i][current_j][2]
         if item_in_next_cell != "":
             new_swag += ["" + item_in_next_cell + ""]
         if len(new_swag) > 1 and new_swag[0] == "":
             new_swag = new_swag[1:]

         distances_paths_and_swags[explore_i][explore_j][0] = new_distance
         distances_paths_and_swags[explore_i][explore_j][1] = new_path
         distances_paths_and_swags[explore_i][explore_j][2] = new_swag
         heappush(vertices_to_explore, (new_distance, explore_i, explore_j))
         count += 1
  return distances_paths_and_swags, count


def quicksort( list, start, end):
  # base condition for this recursive function
  if start >= end:
    return
  # select random element to be pivot
  pivot_idx = randrange(start, end + 1)
  pivot_element = list[pivot_idx]
  #print("privot element: {0}".format(pivot_element))
  # swap random element with last element in sub-listay
  list[end], list[pivot_idx] = list[pivot_idx], list[end]
  # tracks all elements which should be to left (lesser than) pivot
  less_than_pointer = start
  for i in range(start, end):
    if list[i] < pivot_element:
      # swap element to the right-most portion of lesser elements
      list[i], list[less_than_pointer] = list[less_than_pointer], list[i]
      # increase lesser element
      less_than_pointer += 1
  # move pivot element to the right-most portion of lesser elements
  list[end], list[less_than_pointer] = list[less_than_pointer], list[end]
  # Call quicksort on the "left" and "right" sub-lists
  quicksort(list, start, less_than_pointer - 1)
  quicksort(list, less_than_pointer + 1, end)
