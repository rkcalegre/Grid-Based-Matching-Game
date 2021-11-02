import random

def create_grid(M, N, R): #Creates the grid, with initial random numbers
    grid = [ [random.randint(0, R - 1) for n in range(M)] for n in range(N) ]
    return format(grid)

def format(grid): #Formats the grid
    M = len(grid[0])
    N = len(grid)
    row_index = 0

    for row in grid:
        if row_index == 0:
            print('|-----' * M, end='|\n')
        else:
            print('|-----' * M, end='|\n')
        col_index = 0
        for col in row:
            if col_index == 0:
                print('|  ' + str(col), end='  |  ')
            else:
                print(col, end='  |  ')
            col_index += 1
        print('')
        row_index += 1
    print('|-----' * M, end='|\n')
    return grid

def count_adjacent_cells(row, col, grid): #counts number of adjacent cells
    #player_grid = grid.copy()
    M = len(grid[0])
    N = len(grid)
    origin = grid[row][col]
    count = 1

    for x in (-1, 1):
        for y in (-1, 1):
            if row + x > -1 and row + x < N and col + y > -1 and col + y < M:
                if grid[row][col + y] == origin:
                    count += 1
                    if col + y + y > -1 and col + y + y < M:
                        if grid[row][col + y + y] == origin:
                            count += 1
                    if grid[row + x][col + y] == origin:
                        count += 1
                if grid[row + x][col] == origin:
                    count += 1
                    if row + x + x > -1 and row + x + x < N:
                        if grid[row + x + x][col]:
                            count += 1
                    if grid[row + x][col + y] == origin:
                        count += 1

    return count

def del_adjacent_cells(row, col, grid): #empties out the cells adjacent to the cell user input
    player_grid = grid.copy()
    M = len(player_grid[0])
    N = len(player_grid)
    origin = grid[row][col]

    coordinates = [[row, col]]
    for coord in coordinates:
        for a in (-1, 1):
            if (a != -1 or coord[1] != 0) and (a != 1 or coord[1] < (M - 1)):
                adjacent_x = grid[coord[0]][coord[1] + a]
                if adjacent_x == origin:
                    player_grid[coord[0]][coord[1] + a] = ' '
                    player_grid[coord[0]][coord[1]] = ' '
                    coordinates.append([coord[0], coord[1] + a])
            if (a != -1 or coord[0] != 0) and (a != 1 or coord[0] < (N - 1)):
                adjacent_y = grid[coord[0] + a][coord[1]]
                if adjacent_y == origin:
                    player_grid[coord[0] + a][coord[1]] = ' '
                    player_grid[coord[0]][coord[1]] = ' '
                    coordinates.append([coord[0] + a, coord[1]])

    raw_score = len(coordinates)

    return gravity(player_grid), raw_score

def count_score(raw_score): #counts out the score
    score = (raw_score - 2) ** 2
    current_score = score
    return current_score

def gravity(player_grid): #shifts elements down if there is an empty cell below it
    player_grid = player_grid.copy()
    M = len(player_grid[0])
    N = len(player_grid)

    for row in range(N - 1, 0, -1):
        for col in range(0, M):
            if player_grid[row][col] == ' ':
                for above in range(1, N):
                    if row - above == -1:
                        break
                    if player_grid[row - above][col] != ' ':
                        player_grid[row][col] = player_grid[row - above][col]
                        player_grid[row - above][col] = ' '
                        break

    return delete_column(player_grid)

def delete_column(player_grid):
    M = len(player_grid[0])
    N = len(player_grid)

    for col in range(M - 1, -1, -1):
        for row in range(0, N):
            if player_grid[row][col] != ' ':
                break
            if row == N - 1 and player_grid[row][col] == ' ':
                for delete in range(0, N):
                    del player_grid[delete][col]

    return format(player_grid)

def terminate(grid): #Scans the whole grid. If it finds a cell with at least 3 similar neighbors, the loop will terminate.
    M = len(grid[0])
    N = len(grid)

    for row in range(0, N):
        for col in range(0, M):
            if grid[row][col] == ' ': break
            count = count_adjacent_cells(row, col, grid)
            if count >= 3:
                return False #program will continue if the function returns False
    return True #returns true if cell has less than 3 neighbors. this means that the program will terminate

def init_game(): #Begins the game with an initial grid, score, and max number of blocks cleared
    M, N, R = [int(x) for x in input("Enter Game Settings: ").split(',')]
    grid = create_grid(M, N, R)
    current_score = 0
    max_blocks = 0
    game(grid, current_score, max_blocks)

def game(grid, current_score, max_blocks):
    if not terminate(grid): #If True, program will terminate. If not, program will continue
        row, col = [int(x) for x in input("Enter coordinates: ").split(',')]

        #error handling
        if row in range(0, len(grid)) and col in range(0, len(grid[0])) and grid[row][col] == ' ': #checks for empty cell
            print('Input coordinate is empty.')
            return game(grid, current_score, max_blocks)
        if not (row in range(0, len(grid)) and col in range(0, len(grid[0]))): #checks if input is within grid range
            print('Invalid input. Input not in range.')
            return game(grid, current_score, max_blocks)
        else: #game proper
            count = count_adjacent_cells(row, col, grid)
            if count >= 3:
                player_grid, raw_score = del_adjacent_cells(row, col, grid)
                current_score += count_score(raw_score)

                if raw_score > max_blocks:
                    max_blocks = raw_score

                print("Current score: ", current_score)
                return game(grid, current_score, max_blocks)
            else:
                print('Invalid input. Adjacent blocks not greater than two.')
                return game(grid, current_score, max_blocks)
    else:
        print('\nG A M E  E N D E D')
        print("Total score: ", current_score)
        print('Most number of blocks cleared: ', max_blocks)

init_game()