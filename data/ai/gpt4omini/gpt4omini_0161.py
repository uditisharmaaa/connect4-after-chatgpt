import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]

def create_board():
    """Create a board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column letters
    print("+---" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLUMNS)

def valid_input(column, board):
    """Check if the input column is valid for placing a checker."""
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != " ":
        return False
    return True

def place_checker(board, column, checker):
    """Place a checker in the correct position in the column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, checker):
    """Check for a win in the board for the given checker."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    # Print the initial board
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        input_valid = False

        while not input_valid:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            column = ord(column_input) - 65
            
            if valid_input(column, board):
                place_checker(board, column, current_player)
                input_valid = True
            else:
                print("Invalid input. Please try again.")

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
