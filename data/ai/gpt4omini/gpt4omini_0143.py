import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

# Create the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

# Check for valid column input
def is_valid_column(col):
    return (0 <= col < COLUMNS)

# Check if the column is full
def is_column_full(board, col):
    return board[0][col] != ' '

# Place the checker in the column
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if all(row[i + j] == checker for j in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + j][col] == checker for j in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + j][col + j] == checker for j in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - j][col + j] == checker for j in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ")
        column_input = input().strip().upper()
        
        if len(column_input) != 1 or not ('A' <= column_input <= chr(65 + COLUMNS - 1)):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        
        column = ord(column_input) - 65
        
        if not is_valid_column(column):
            print("Invalid column. Please try again.")
            continue
        
        if is_column_full(board, column):
            print("Column is full. Please try again.")
            continue
        
        # Place checker
        place_checker(board, column, checker)

        # Check for win
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
