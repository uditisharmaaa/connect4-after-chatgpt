import os
import random

# Constants for the board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create the Connect 4 board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input():
    """Get a valid column input from the player."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            return ord(column) - 65  # Convert column letter to index
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, player):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # Column is full

def check_winner(board, player):
    """Check if the current player has won the game."""
    # Check horizontal, vertical, and diagonal (both directions)

    # Check horizontal
    for row in board:
        count = 0
        for cell in row:
            count = count + 1 if cell == player else 0
            if count >= 4:
                return True

    # Check vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            count = count + 1 if board[r][c] == player else 0
            if count >= 4:
                return True

    # Check diagonal (left to right)
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS) and (r + 3 < ROWS):
                if all(board[r + i][c + i] == player for i in range(4)):
                    return True

    # Check diagonal (right to left)
    for r in range(ROWS):
        for c in range(COLS):
            if (c - 3 >= 0) and (r + 3 < ROWS):
                if all(board[r + i][c - i] == player for i in range(4)):
                    return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
if __name__ == "__main__":
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select the first player

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]

        # Get a valid move
        column = get_valid_input()

        # Place the checker
        if place_checker(board, column, current_player):
            # Check for win
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            # Check for draw
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            # Switch to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Please choose another column.")
