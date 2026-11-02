import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check for a win
def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if c <= COLUMNS - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if r >= 3 and c <= COLUMNS - 4 and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Validate input
def validate_input(column_choice):
    if len(column_choice) == 1 and "A" <= column_choice <= chr(64 + COLUMNS):
        return True
    return False

# Play the game
def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        column_choice = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if not validate_input(column_choice):
            print("Invalid input, please try again.")
            continue

        column_number = ord(column_choice) - 65
        if board[0][column_number] != " ":
            print("Column is full, turn is lost.")
            current_player = (current_player + 1) % PLAYERS
            continue

        for row in range(ROWS-1, -1, -1):
            if board[row][column_number] == " ":
                board[row][column_number] = CHECKERS[current_player]
                break

        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
