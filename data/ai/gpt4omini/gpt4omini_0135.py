import os
import random

# Constants for the board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Support for up to 5 players

def initialize_board():
    """Creates and returns an empty board with the defined dimensions."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_input(player):
    """Prompt the player for a valid column input."""
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(64 + COLUMNS)}): ").upper()
        if len(column) == 1 and 'A' <= column <= chr(64 + COLUMNS):
            col_index = ord(column) - 65
            return col_index
        print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    """Places the checker in the specified column if possible."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the given checker has a winning combination on the board."""
    # Check all possible winning combinations: horizontal, vertical, diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                # Horizontal
                if c <= COLUMNS - 4 and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Vertical
                if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Diagonal /
                if r >= 3 and c <= COLUMNS - 4 and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
                # Diagonal \
                if r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the board is full without any winners."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop for Connect 4."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)

    while True:
        print_board(board)
        column = get_valid_input(current_player)

        if not place_checker(board, column, current_player):
            print("Column is full, try a different column.")
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
