import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # For simplicity, use 2 players

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_player_move(player):
    """Get a valid column input from the player."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) == 1 and 'A' <= move <= chr(65 + COLS - 1):
            return ord(move) - 65
        else:
            print("Invalid input. Please enter a column (A, B, C, ...).")

def place_checker(board, col, player):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal, vertical, and diagonal connections
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Diagonal check (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    # Diagonal check (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select first player
    print_board(board)

    while True:
        col = get_player_move(current_player)
        if place_checker(board, col, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full! Try a different column.")

if __name__ == "__main__":
    main()
