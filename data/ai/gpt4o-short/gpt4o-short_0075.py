import random
import os

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'] # Max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLUMNS + 1))

def is_valid_column(choice):
    return choice.upper() in COLUMN_LABELS

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game(num_players):
    board = create_board()
    print_board(board)

    current_player = random.randint(0, num_players - 1)
    print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn.")

    while True:
        col_choice = input(f"Player {PLAYER_SYMBOLS[current_player]}, select a column (A-G): ").strip().upper()
        if not is_valid_column(col_choice):
            print("Invalid column. Please try again.")
            continue

        col = COLUMN_LABELS.index(col_choice)
        row = get_next_open_row(board, col)
        if row is None:
            print("Column is full. Please try again.")
            continue

        drop_piece(board, row, col, PLAYER_SYMBOLS[current_player])
        print_board(board)

        if winning_move(board, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} wins!")
            break

        if is_draw(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % num_players
        print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn.")

# Set the number of players (2 to 5)
NUM_PLAYERS = 2  # Adjust this between 2 to 5 as needed

if __name__ == "__main__":
    play_game(NUM_PLAYERS)
