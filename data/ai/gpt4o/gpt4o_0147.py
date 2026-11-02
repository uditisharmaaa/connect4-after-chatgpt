import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

# Initialize the game board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the game board
def print_board(board):
    os.system('clear')
    column_labels = "  ".join(chr(i + 65) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check if input is valid
def is_valid_input(choice, board):
    if choice.isalpha():
        col = ord(choice.upper()) - 65
        if 0 <= col < len(board[0]):
            return True
    return False

# Drop a checker into the specified column
def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + i][col + 3 - i] == checker for i in range(4)):
                return True

    return False

# Check for a draw condition
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)
    while True:
        current_checker = CHECKERS[current_player_idx]
        choice = input(f"Player {current_checker}, please enter a column: ").strip()

        if not is_valid_input(choice, board):
            print("Invalid input. Please try again.")
            continue

        col = ord(choice.upper()) - 65
        if not drop_checker(board, col, current_checker):
            print(f"Column {choice.upper()} is full. Turn lost.")
        else:
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

# Start the game
play_game()
