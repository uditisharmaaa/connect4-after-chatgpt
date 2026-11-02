import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can modify this for more players

def initialize_board():
    """Create the Connect 4 board initialized with whitespace."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A-G
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_valid_input(player):
    """Get valid input from the player for their move."""
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if column in map(chr, range(65, 65 + COLS)):
            return ord(column) - 65
        print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    """Place the checker in the specified column."""
    for row in reversed(board):  # Start checking from the bottom row
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4))) or \
               (r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4))) or \
               (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    """Check for a draw condition."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)  # Randomly select the first player

    print_board(board)

    while True:
        column = get_valid_input(current_player)
        if not place_checker(board, column, current_player):
            print("Column is full! Try another one.")
            continue

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]  # Switch players

if __name__ == "__main__":
    main()
