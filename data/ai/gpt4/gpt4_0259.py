import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    """Create and return an empty board with given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board in the specified format."""
    os.system('clear')  # Clear the screen
    column_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Check if the given column is valid and not full."""
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def get_column_input(board):
    """Prompt the player for a column input and validate it."""
    while True:
        try:
            player_input = input("Please enter a column letter: ").strip().upper()
            if len(player_input) != 1 or not player_input.isalpha():
                raise ValueError("Input must be a single letter.")
            column = ord(player_input) - 65  # Convert letter to column index
            if not is_valid_column(column, board):
                raise ValueError("Invalid column input or column is full.")
            return column
        except ValueError as e:
            print(e)

def drop_checker(board, column, checker):
    """Place the checker in the lowest available space in the given column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_for_winner(board, rows, cols, streak_length=4):
    """Check if there is a winner (4 in a row) on the board."""
    # Check horizontal
    for r in range(rows):
        for c in range(cols - streak_length + 1):
            if board[r][c] != " " and all(board[r][c] == board[r][c + i] for i in range(streak_length)):
                return board[r][c]

    # Check vertical
    for r in range(rows - streak_length + 1):
        for c in range(cols):
            if board[r][c] != " " and all(board[r][c] == board[r + i][c] for i in range(streak_length)):
                return board[r][c]

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - streak_length + 1):
        for c in range(cols - streak_length + 1):
            if board[r][c] != " " and all(board[r][c] == board[r + i][c + i] for i in range(streak_length)):
                return board[r][c]

    # Check diagonal (top-left to bottom-right)
    for r in range(streak_length - 1, rows):
        for c in range(cols - streak_length + 1):
            if board[r][c] != " " and all(board[r][c] == board[r - i][c + i] for i in range(streak_length)):
                return board[r][c]
    return None

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Game initialization
    players = MIN_PLAYERS  # Number of players (can be modified if needed)
    board = initialize_board(ROWS, COLUMNS)
    player_symbols = PLAYER_SYMBOLS[:players]
    random.shuffle(player_symbols)
    current_player_idx = 0

    print_board(board)
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(player_symbols)}")
    print(f"Randomly starting with Player {player_symbols[current_player_idx]}")

    # Game loop
    while True:
        print_board(board)
        current_player = player_symbols[current_player_idx]
        print(f"Player {current_player}'s turn.")
        
        column = get_column_input(board)
        drop_checker(board, column, current_player)

        # Check for a winner
        winner = check_for_winner(board, ROWS, COLUMNS)
        if winner:
            print_board(board)
            print(f"Player {winner} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % players

if __name__ == "__main__":
    main()
