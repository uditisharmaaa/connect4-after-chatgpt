import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players as specified
NUM_PLAYERS = 2  # You can adjust this for larger games

def create_board():
    """Create and return a new empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(board, column):
    """Check whether dropping a checker in the given column is valid."""
    return board[0][column] == " "

def apply_move(board, column, player):
    """Apply a move to the board for the given player in the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            break

def is_winner(board, player):
    """Check if the specified player has a winning line."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(all(cell != " " for cell in row) for row in board)

def get_column_choice():
    """Prompt the player for a valid column choice."""
    while True:
        choice = input("Please enter a column: ").strip().upper()
        if choice and len(choice) == 1 and 'A' <= choice <= 'G':
            return ord(choice) - ord('A')
        print("Invalid input. Please enter a letter between A and G.")

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        print(f"Player {PLAYERS[current_player_index]}, it's your turn.")
        
        column = get_column_choice()

        if not is_valid_move(board, column):
            print("Column is full or invalid choice. Try again.")
            continue

        apply_move(board, column, PLAYERS[current_player_index])
        print_board(board)

        if is_winner(board, PLAYERS[current_player_index]):
            print(f"Player {PLAYERS[current_player_index]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
