import os
import random

# Constants for the game, adjusts the number of players and their symbols.
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change this between 2 to 5
PLAYERS = PLAYERS[:NUM_PLAYERS]

ROWS = 6
COLS = 7
COLUMNS_LABELS = [chr(i) for i in range(65, 72)]  # Labels 'A', 'B', 'C', etc.

def initialize_board():
    """Initializes the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current board state."""
    os.system('clear')
    print("  " + " ".join(COLUMNS_LABELS))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("  " + "---" * COLS)

def input_valid(move):
    """Checks if the player's input is valid."""
    return move in COLUMNS_LABELS

def is_column_full(board, col):
    """Checks if a column is full."""
    return board[0][col] != ' '

def drop_piece(board, col, piece):
    """Drops a piece into the selected column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = piece
            break

def check_win(board, piece):
    """Checks all directions for a connect-4 win."""

    # Check horizontal win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == piece:
                return True

    # Check vertical win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == piece:
                return True

    return False

def check_draw(board):
    """Checks if the board is full and the game is a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = initialize_board()
    player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        player = PLAYERS[player_index]
        print(f"Player {player}'s turn")

        move = input(f"Choose a column ({' '.join(COLUMNS_LABELS)}): ").upper()
        
        if not input_valid(move):
            print("Invalid input. Please choose a valid column.")
            continue

        col = COLUMNS_LABELS.index(move)
        
        if is_column_full(board, col):
            print("Column is full. Choose a different column.")
            continue

        drop_piece(board, col, player)

        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        player_index = (player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
