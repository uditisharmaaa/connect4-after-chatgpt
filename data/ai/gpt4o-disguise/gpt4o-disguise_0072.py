import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
MAX_COLUMNS = 26

# Player markers
player_markers = ['X', 'O', 'V', 'H', 'M']
available_players = player_markers[:PLAYERS]

# Initialize board
board = [[' ' for _ in range(ROWS)] for _ in range(COLUMNS)]

# Clear screen
def clear_screen():
    os.system('clear')

# Print board
def print_board():
    clear_screen()
    headers = " ".join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {headers}")
    print("+---" * COLUMNS + "+")
    for row in range(ROWS):
        row_str = "|".join(f" {board[col][row]} " for col in range(COLUMNS))
        print(f"|{row_str}|")
        print("+---" * COLUMNS + "+")

# Check for win
def check_win():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[col][row] != ' ':
                # Horizontal check
                if col <= COLUMNS - 4 and all(board[col + i][row] == board[col][row] for i in range(4)):
                    return True
                # Vertical check
                if row <= ROWS - 4 and all(board[col][row + i] == board[col][row] for i in range(4)):
                    return True
                # Diagonal down-right check
                if col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[col + i][row + i] == board[col][row] for i in range(4)):
                    return True
                # Diagonal up-right check
                if col <= COLUMNS - 4 and row >= 3 and all(board[col + i][row - i] == board[col][row] for i in range(4)):
                    return True
    return False

# Check for draw
def check_draw():
    return all(board[col][0] != ' ' for col in range(COLUMNS))

# Place checker
def place_checker(column, marker):
    for row in reversed(range(ROWS)):
        if board[column][row] == ' ':
            board[column][row] = marker
            return True
    return False

# Get valid input
def get_valid_input():
    while True:
        user_input = input(f"Player {current_marker}, please enter a column: ").strip().upper()
        if len(user_input) == 1 and user_input.isalpha():
            column_index = ord(user_input) - 65
            if 0 <= column_index < COLUMNS:
                return column_index
        print("Invalid input. Please enter a valid column letter.")

# Main game loop
random.shuffle(available_players)
current_player_index = random.randint(0, PLAYERS - 1)
current_marker = available_players[current_player_index]

# Initial board print
print_board()

while True:
    column = get_valid_input()
    
    if place_checker(column, current_marker):
        print_board()
        if check_win():
            print(f"Player {current_marker} won!")
            break
        elif check_draw():
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS
        current_marker = available_players[current_player_index]
    else:
        print("Column is full, try another.")
