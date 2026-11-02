import os
import random

# Constants for the game dimensions and players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the terminal for better visualization
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A-G
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(column, board):
    """Check if the chosen column is valid for placing a checker."""
    if column >= COLS or column < 0:
        return False  # Out of bounds
    if board[0][column] != " ":
        return False  # Column is full
    return True

def drop_checker(board, column, checker):
    """Place a checker in the selected column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, checker):
    """Check if the current player has won."""
    # Check horizontal, vertical, and diagonal (both directions) for 4 in a row
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    """Main game loop for Connect 4."""
    board = initialize_board()
    players = CHECKERS[:2]  # Use only the first two checkers for this assignment
    current_player_index = random.randint(0, len(players) - 1)  # Randomly select the first player

    print_board(board)
    
    while True:
        current_player = players[current_player_index]
        valid_move = False

        while not valid_move:
            try:
                column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
                column = ord(column_input) - 65  # Convert letter A-G to index 0-6
                if is_valid_input(column, board):
                    drop_checker(board, column, current_player)
                    valid_move = True
                else:
                    print("Invalid input. Please choose a valid column.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a column between A and G.")

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    main()
