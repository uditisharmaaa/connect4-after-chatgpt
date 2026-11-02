import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

def create_board():
    """Create an empty board with the given dimensions."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_player_input(player):
    """Get and validate input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if column in COLUMN_LABELS:
            return COLUMN_LABELS.index(column)
        else:
            print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_for_win(board, checker):
    """Check for a win in any direction."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    """Check if the board is in a draw state."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(CHECKERS)
    print_board(board)
    
    while True:
        column = get_player_input(current_player)
        if place_checker(board, column, current_player):
            print_board(board)
            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_for_draw(board):
                print("The game is a draw!")
                break
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full. Turn is lost.")

if __name__ == "__main__":
    main()
