import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65+i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Get the next open row in a column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

# Check if the input column is valid
def validate_input(column, board):
    if len(column) != 1 or not ('A' <= column <= chr(64 + COLUMNS)):
        return False
    col_idx = ord(column) - 65
    if get_next_open_row(board, col_idx) is None:
        return False
    return True

# Check for a win
def check_for_win(board, checker):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    
    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_for_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    
    print_board(board)

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        column = input().strip()

        if validate_input(column, board):
            col_index = ord(column) - 65
            row_index = get_next_open_row(board, col_index)

            board[row_index][col_index] = current_checker
            print_board(board)

            if check_for_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_for_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
