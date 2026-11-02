import os
import random

# Constants for the game
ROWS = 6
COLS = 7
LABELS = ["A", "B", "C", "D", "E", "F", "G"]
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Set the number of players (between 2 and 5)
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5 based on your requirement

def initialize_board():
    return [[' ']*COLS for _ in range(ROWS)]

def display_board(board):
    os.system('clear')  # Clear the console
    print(" " + " ".join(LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("="*(COLS * 2 + 1))

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == ' ':
            return r
    return None

def is_valid_column(col_input):
    return col_input in LABELS

def place_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def connect_4():
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        display_board(board)
        current_player = PLAYER_SYMBOLS[current_player_index]
        col_input = input(f"Player {current_player}, make your selection (A-G): ").upper()

        if not is_valid_column(col_input):
            print(f"Invalid input! Please choose between columns {', '.join(LABELS)}.")
            continue

        col = LABELS.index(col_input)
        row = get_next_open_row(board, col)

        if row is None:
            print("This column is full! Please choose another column.")
            continue

        place_piece(board, row, col, current_player)

        if winning_move(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif is_draw(board):
            display_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_4()
