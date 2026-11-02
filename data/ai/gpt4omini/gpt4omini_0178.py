import os
import random

# Constants for the game
ROWS = 6           # Number of rows in the board
COLS = 7           # Number of columns in the board
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player checkers

def create_board():
    """Creates a 2D board initialized with whitespace."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * (COLS))
    
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS))

def is_valid_input(col_input):
    """Checks if the user input is valid and return the column index."""
    if len(col_input) != 1:
        return False
    if col_input.upper() < 'A' or col_input.upper() >= chr(65 + COLS):
        return False
    return True

def get_column_index(col_input):
    """Returns the column index for the given character input."""
    return ord(col_input.upper()) - 65

def drop_checker(board, col, checker):
    """Drops a checker into the specified column and returns the row index or -1 if invalid."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full

def check_winner(board, checker):
    """Checks if the specified player has won the game."""
    # Check horizontal, vertical, and diagonal matches
    for row in range(ROWS):
        for col in range(COLS):
            if (check_direction(board, row, col, checker, 1, 0) or  # Horizontal
                check_direction(board, row, col, checker, 0, 1) or  # Vertical
                check_direction(board, row, col, checker, 1, 1) or  # Diagonal /
                check_direction(board, row, col, checker, 1, -1):   # Diagonal \
                return True
    return False

def check_direction(board, row, col, checker, delta_row, delta_col):
    """Check for four in a row in a specific direction."""
    count = 0
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def is_draw(board):
    """Checks if the board is full."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Random first player
    print(f"Player {PLAYERS[current_player_index]} will start the game.")
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        
        while True:
            column_input = input(f"Player {current_player}, please enter a column: ")
            if is_valid_input(column_input):
                col_index = get_column_index(column_input)
                if drop_checker(board, col_index, current_player) != -1:
                    break  
                else:
                    print("Column is full. Choose another column.")
            else:
                print("Invalid input. Please enter a valid column (A-G).")
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
