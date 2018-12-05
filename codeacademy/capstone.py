from random import randint
from math import inf
from maze import build_maze, explore_maze, print_maze_paths, mow
from graph import dijkstras, a_star, bfs, quicksort
from colors import colors


#define grid size
grid_size_row = 15
grid_size_colmun = 35

#swag list
swags = ['*', '+', 'candy corn', 'werewolf', 'pumpkin', 'apple', 'banana', 'diamond', 'melon', 'watermelon', 'kiwi']

# building maze
grid, start_i, start_j, end_i, end_j = build_maze(grid_size_row, grid_size_colmun, swags)

# rendering maze
print( colors.CBLUE2 + "   ## Maze ## " + colors.CEND )
print_maze_paths(grid, None)
print("\nGrid size row: {0}, column: {1}".format(grid_size_row, grid_size_colmun))
print("Start point: {0},{1}\nEnd point: {2},{3}".format(start_i, start_j, end_i, end_j))

# run dijkstras's algorithm to find a path to the end
paths_and_distances, count = dijkstras(grid, start_i, start_j)
print("\n" + colors.CBLUE2 + "   ## Dijkstras ## " + colors.CEND)
print_maze_paths(grid, paths_and_distances[end_i][end_j][1])

# Debug only
#print("\ndistances for each cell:\n")
#for row in paths_and_distances:
#    for column in row:
#        if column[0] == inf:
#            column[0] = "|||"
#        print("{:3}".format(column[0]), end = " ")
#    print(" ")
#print("\nDistance from Start to End is {0}".format(paths_and_distances[end_i][end_j][0]))
print("Found the end of the in the {0} steps with length of {1}".format(count, len(paths_and_distances[end_i][end_j][1])))

# run a* algorithm
paths_distances_and_swags, count = a_star(grid, start_i, start_j, end_i, end_j)

print("\n" + colors.CBLUE2 + "   ## A star ## " + colors.CEND)
print_maze_paths(grid, paths_distances_and_swags[end_i][end_j][1])

# Debug only
#print("\ndistances with hueristic for each cell:\n")
#for row in paths_distances_and_swags:
#    for column in row:
#        if column[0] == inf:
#            column[0] = "|||"
#        print("{:3.3}".format(str(column[0])), end = " ")
#    print(" ")
#print("\nDistance from Start to End is {0}".format(paths_distances_and_swags[end_i][end_j][0]))
print("Found the end of the in the {0} steps with length of {1}".format(count, len(paths_distances_and_swags[end_i][end_j][1])))
#print("Path from Start to End: \n{0}".format(paths_distances_and_swags[end_i][end_j][1]))

print("\n" + colors.CBLUE2 + "   ## BFS ## " + colors.CEND)
paths_and_swags, count = bfs(grid, start_i, start_j, swags)
print_maze_paths(grid, paths_and_swags[end_i][end_j][0])
print("Found the end of the in the {0} steps with length of {1}".format(count, len(paths_and_swags[end_i][end_j][0])))


swag_list = paths_distances_and_swags[end_i][end_j][2]
print("\nSwags collected along the way: \n{0}".format(swag_list))
quicksort(swag_list, 0, len(swag_list) - 1)
print("Sorted Swag list by quick sort: \n{0}".format(swag_list))

#print("\n\nShortest Distances: {0}".format(distances))
