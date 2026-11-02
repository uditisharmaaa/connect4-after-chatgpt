import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Use only first PLAYERS checkers

def create_board():
    """Create a board with predefined dimensions."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    for i in range(COLUMNS):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()
    for row in board:
        print("+---" * COLUMNS + "+")
        for cell in row:
            print(f"| {cell} ", end="")
        print("|")
    print("+---" * COLUMNS + "+")
    
def is_valid_column_input(input_char):
    """Check if the entered column input is valid."""
    return input_char.isalpha() and ord(input_char) - ord('A') < COLUMNS

def drop_checker(board, column, checker):
    """Drop a checker into the selected column."""
    row_index = None
    # Find the lowest empty space in the column
    for row in reversed(board):
        if row[column] == " ":
            row_index = board.index(row)
            break
    # If there's a valid row index, place the checker
    if row_index is not None:
        board[row_index][column] = checker
        return True
    return False

def check_win(board, checker):
    """Check for a win condition."""
    # Check horizontal, vertical, and diagonal lines
    # Horizontal Check
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True
    
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Diagonal Check (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Diagonal Check (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the board is full, leading to a draw."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        while True:
            column_input = input().strip().upper()
            if is_valid_column_input(column_input):
                column_index = ord(column_input) - ord('A')
                if drop_checker(board, column_index, current_checker):
                    break
                else:
                    print(f"Column {column_input} is full, choose another column.")
            else:
                print("Invalid input, please enter a valid column letter.")
        
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
