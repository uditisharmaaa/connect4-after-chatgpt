import os
import random

# Constants representing players
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Constants for the grid
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_grid():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_grid(grid):
    os.system('clear')  # Use 'cls' if on Windows
    print("  " + " ".join(COLUMN_LABELS))
    for row in grid:
        print("| " + " | ".join(row) + " |")
    print("-" * (COLUMNS * 4 + 1))

def is_valid_column(column, grid):
    if column not in COLUMN_LABELS:
        return False
    index = COLUMN_LABELS.index(column)
    return grid[0][index] == ' '

def drop_disc(grid, column, player):
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(grid):
        if row[col_index] == ' ':
            row[col_index] = player
            break

def check_win_condition(grid, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(grid[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(grid[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(grid[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(grid[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(grid):
    return all(cell != ' ' for row in grid for cell in row)

def play_game(num_players):
    grid = create_grid()
    current_player_index = random.randint(0, num_players - 1)
    players = PLAYERS[:num_players]

    while True:
        current_player = players[current_player_index]
        print_grid(grid)
        column = input(f"Player {current_player}, enter your move (A-G): ").strip().upper()

        if not is_valid_column(column, grid):
            print("Invalid move. Please try again.")
            continue

        drop_disc(grid, column, current_player)

        if check_win_condition(grid, current_player):
            print_grid(grid)
            print(f"Player {current_player} wins!")
            break

        if check_draw(grid):
            print_grid(grid)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    num_players = int(input("Enter number of players (2-5): "))
    if num_players < 2 or num_players > 5:
        print("Invalid number of players. Please choose between 2 and 5.")
    else:
        play_game(num_players)
