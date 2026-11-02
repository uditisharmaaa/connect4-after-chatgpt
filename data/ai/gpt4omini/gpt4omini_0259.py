import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Creates a 2D list representing the game board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board to the terminal."""
    os.system('clear')  # Clear the screen (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(column):
    """Checks if the input column is valid (A-G)."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Converts a column letter to its index (0-6)."""
    return ord(column) - 65

def is_column_full(board, col_idx):
    """Checks if the specified column is full."""
    return board[0][col_idx] != ' '

def drop_checker(board, col_idx, checker):
    """Drops a checker in the specified column."""
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return

def check_winner(board, checker):
    """Checks if the specified checker has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (i.e., the board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(range(len(PLAYERS)))  # Randomly select the first player

    while True:
        print_board(board)
        player_checker = PLAYERS[current_player]
        column = input(f"Player {player_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        # Validate input
        while not is_valid_input(column):
            column = input(f"Invalid input. Player {player_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        col_idx = get_column_index(column)

        # Check if column is full
        if is_column_full(board, col_idx):
            print("Column is full! Please choose another column.")
            continue
        
        # Drop the checker
        drop_checker(board, col_idx, player_checker)

        # Check for win
        if check_winner(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player = (current_player + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
