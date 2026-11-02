import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(c) for c in range(65, 65 + COLS)))  # Column labels A-G
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column):
    """Check if the input column is valid."""
    return len(column) == 1 and column.isalpha() and "A" <= column < chr(65 + COLS)

def is_column_full(board, col_index):
    """Checks if a column is full."""
    return board[0][col_index] != " "

def drop_checker(board, col_index, checker):
    """Drops the checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return

def check_winner(board, checker):
    """Checks for a win condition with the given checker."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
                
    return False

def check_draw(board):
    """Checks if the board is full and the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Initialize game variables
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYER_COUNT)]
    current_player_index = random.randint(0, PLAYER_COUNT - 1)

    # Print the initial board
    print_board(board)

    while True:
        # Get current player
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        # Input validation
        while True:
            column_input = input().upper()
            if not is_valid_column(column_input):
                print("Invalid input. Please enter a column letter (A-G):")
                continue
            
            column_index = ord(column_input) - 65
            if is_column_full(board, column_index):
                print("Column is full. Please choose another column:")
                continue
            
            break
        
        # Place the checker
        drop_checker(board, column_index, current_player)
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
