from random import randint
from colors import colors
from graph import new_position_after_move

directions = ["U", "D", "L", "R"]

def build_maze(m, n, swag):
  grid = []
  for i in range(m):
    row = []
    for j in range(n):
      row.append("wall")
    grid.append(row)
  start_i = randint(0, m-1)
  start_j = randint(0, n-1)
  mow(grid, start_i, start_j)
  grid[start_i][start_j] = "start"
  end_i, end_j = explore_maze(grid, start_i, start_j, swag)
  return grid, start_i, start_j, end_i, end_j

def explore_maze(grid, start_i, start_j, swag):
  grid_copy = [row[:] for row in grid]
  bfs_queue = [[start_i, start_j]]

  while bfs_queue:
    i,j = bfs_queue.pop(0)
    if grid[i][j] != "start" and randint(1,10) == 1:
      grid[i][j] = swag[randint(0, len(swag) - 1)]
    grid_copy[i][j] = "visited"
    for direction in directions:
      explore_i, explore_j = new_position_after_move(i, j, direction)
      if explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0]):
         continue
      elif grid_copy[explore_i][explore_j] != "wall" and grid_copy[explore_i][explore_j] != "visited":
        bfs_queue.append([explore_i, explore_j])
  grid[i][j] = "end"
  return i, j

def print_maze_paths(grid, paths):
   row_count = 0
   for row in grid:
    printable_row = ""

    # print header of rows and columns with number
    column_count = 0
    for cell in row:
        if row_count == 0:
          char = ''
          if column_count == 0:
            char = ' '
          char += colors.CGREYBG + str(column_count)[-1] + colors.CEND
        else:
          break
        printable_row += char
        column_count += 1
    if row_count == 0:
      print(printable_row)
    printable_row = ""

    # print cell of maze
    column_count = 0
    for cell in row:
      if cell == "wall":
        char = '|'
      elif cell == "empty":
        char = ' '
        current_position = "(" + str(row_count) + "," + str(column_count) + ")"
        if paths != None and current_position in paths:
          char = colors.CYELLOWBG2 + ' ' + colors.CEND
      else:
        char = cell[0]
        current_position = "(" + str(row_count) + "," + str(column_count) + ")"
        if char == 's':
          char = colors.CREDBG + 'S' + colors.CEND
        elif char == 'e':
          char = colors.CGREENBG + 'E' + colors.CEND
        elif paths != None and current_position in paths:
          char = colors.CYELLOWBG2 + cell[0] + colors.CEND
      if column_count == 0:
          char = colors.CGREYBG + str(row_count)[-1] + colors.CEND + char
      printable_row += char
      column_count += 1
    print(printable_row)
    row_count += 1

def mow(grid, i, j):
  directions = ["U", "D", "L", "R"]
  while directions:
    directions_index = randint(0, len(directions) - 1)
    direction = directions.pop(directions_index)
    if direction == "U":
      if i - 2 < 0:
        continue
      elif grid[i-2][j] == "wall":
        grid[i-1][j] = "empty"
        grid[i-2][j] = "empty"
        mow(grid, i-2, j)
    elif direction == "D":
      if i + 2 >= len(grid):
        continue
      elif grid[i+2][j] == "wall":
        grid[i+1][j] = "empty"
        grid[i+2][j] = "empty"
        mow(grid, i+2, j)
    elif direction == "L":
      if j - 2 < 0:
        continue
      elif grid[i][j-2] == "wall":
        grid[i][j-1] = "empty"
        grid[i][j-2] = "empty"
        mow(grid, i, j-2)
    elif direction == "R":
      if j + 2 >= len(grid[0]):
        continue
      elif grid[i][j+2] == "wall":
        grid[i][j+1] = "empty"
        grid[i][j+2] = "empty"
        mow(grid, i, j+2)
