import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print board function
def print_board(board):
    os.system('clear')
    column_labels = "  ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print("  " + column_labels)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

# Get valid column input
def get_valid_column(board):
    while True:
        try:
            column_input = input("Please enter a column: ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                raise ValueError("Input must be a single letter.")
            column_index = ord(column_input) - ord('A')
            if column_index < 0 or column_index >= len(board[0]):
                raise ValueError("Input must be within the board range.")
            if all(row[column_index] != " " for row in board):  # Column full
                raise ValueError("Column is full.")
            return column_index
        except ValueError as e:
            print(e)

# Place checker in board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

# Check for win
def check_for_win(board, checker):
    # Check horizontal, vertical, diagonal
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col + 3 < COLUMNS and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row+i][col] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if row - 3 >= 0 and col + 3 < COLUMNS and all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

# Check for draw
def check_for_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

# Main game function
def play_game():
    board = create_board(ROWS, COLUMNS)
    players = 2  # Number of players
    checkers = CHECKERS[:players]
    current_player = random.choice(checkers)
    
    # Initial board display
    print_board(board)
    print(f"Player {current_player}, it's your turn.")

    while True:
        column_index = get_valid_column(board)
        place_checker(board, column_index, current_player)
        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player = checkers[(checkers.index(current_player) + 1) % players]
        print(f"Player {current_player}, it's your turn.")

if __name__ == "__main__":
    play_game()
