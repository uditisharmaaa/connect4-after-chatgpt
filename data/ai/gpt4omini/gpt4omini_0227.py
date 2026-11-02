import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    """Creates a board initialized with whitespace."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current board state."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))  # Column labels A-G
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def valid_input(column):
    """Checks if the input column is valid."""
    if len(column) != 1 or column not in (chr(65 + i) for i in range(COLS)):
        return False
    return True

def get_column_index(column):
    """Returns the index of the column based on letter input."""
    return ord(column) - 65

def place_checker(board, column, checker):
    """Places the checker in the specified column and returns True if successful."""
    col_index = get_column_index(column)
    for row in reversed(board):  # Start from the bottom of the column
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Checks if the specified checker has won the game."""
    # Check horizontal, vertical, and diagonal (both directions) for 4 in a row
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                if col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)):  # Horizontal
                    return True
                if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):  # Vertical
                    return True
                if col <= COLS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == checker for i in range(4)):  # Diagonal \
                    return True
                if col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == checker for i in range(4)):  # Diagonal /
                    return True
    return False

def check_draw(board):
    """Checks if the board is full for a draw condition."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column (A-G): ", end="")
        column = input().upper()
        
        while not valid_input(column):
            print("Invalid input. Please enter a valid column (A-G): ", end="")
            column = input().upper()
        
        if place_checker(board, column, current_player):
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            
            # Switch to the next player
            current_index = PLAYERS.index(current_player)
            current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]
        else:
            print("Column is full! Try again.")

if __name__ == "__main__":
    main()
