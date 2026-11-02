import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the screen."""
    os.system('clear')

def create_board(rows, columns):
    """Initialize the board as a 2D list with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    
    # Print rows of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(board, column):
    """Check if a column is valid and not full."""
    if column < 0 or column >= len(board[0]):  # Out of bounds
        return False
    return board[0][column] == " "  # Top cell empty?

def find_row_for_column(board, column):
    """Find the lowest empty row in a given column."""
    for row in reversed(range(len(board))):
        if board[row][column] == " ":
            return row
    return None  # Column full

def check_winner(board, player_checker):
    """Check for a winner."""
    # Check horizontal, vertical, and diagonal (both directions)
    for row in range(len(board)):
        for col in range(len(board[0])):
            # Horizontal
            if col + 3 < len(board[0]) and all(board[row][col + i] == player_checker for i in range(4)):
                return True
            # Vertical
            if row + 3 < len(board) and all(board[row + i][col] == player_checker for i in range(4)):
                return True
            # Diagonal \
            if row + 3 < len(board) and col + 3 < len(board[0]) and all(board[row + i][col + i] == player_checker for i in range(4)):
                return True
            # Diagonal /
            if row + 3 < len(board) and col - 3 >= 0 and all(board[row + i][col - i] == player_checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    # Create the board
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    while True:
        # Get the current player checker symbol
        current_player = players[current_player_index]
        
        # Ask the player for input
        while True:
            column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if len(column_input) == 1 and column_input.isalpha():
                column_index = ord(column_input) - 65
                if is_valid_column(board, column_index):
                    break
            print("Invalid input! Please try again.")

        # Place the checker
        row_index = find_row_for_column(board, column_index)
        board[row_index][column_index] = current_player
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
