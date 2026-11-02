import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # Use 'cls' for Windows

def create_board(rows, cols):
    """Creates a new board with given dimensions, initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal."""
    clear_screen()
    cols_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {cols_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(input_char, max_columns):
    """Checks if the input is valid."""
    return len(input_char) == 1 and 'A' <= input_char <= chr(65 + max_columns - 1)

def find_position(board, column):
    """Finds the lowest available position in a given column."""
    for i in range(len(board) - 1, -1, -1):
        if board[i][column] == " ":
            return i
    return None  # Column is full

def place_checker(board, column, checker):
    """Places a checker in the specified column."""
    position = find_position(board, column)
    if position is not None:
        board[position][column] = checker
        return True
    return False

def has_player_won(board, checker, rows, cols):
    """Checks if the given checker has won."""
    # Horizontal check
    for row in range(rows):
        for col in range(cols - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    
    # Vertical check
    for col in range(cols):
        for row in range(rows - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # Diagonal check (top left to bottom right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # Diagonal check (bottom left to top right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    
    return False

def is_board_full(board):
    """Checks if the board is full."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Initialize board and variables
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column: ")
        player_input = input().strip().upper()

        # Validate player input
        if not is_valid_input(player_input, COLUMNS):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        column = ord(player_input) - 65  # Convert column letter to index

        # Place checker if possible, otherwise lose turn
        if place_checker(board, column, current_checker):
            # Check for win
            if has_player_won(board, current_checker, ROWS, COLUMNS):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if is_board_full(board):
                print_board(board)
                print("The game is a draw!")
                break

            # Switch players
            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print("Column is full. You lose your turn.")

if __name__ == "__main__":
    main()
