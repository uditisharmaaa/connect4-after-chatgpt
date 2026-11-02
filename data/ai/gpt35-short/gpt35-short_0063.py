import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = 'ABCDEFG'
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Set number of players here (change between 2 and 5)
NUM_PLAYERS = 3  # example: 3 players (X, O, V)

assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS, f"NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}"

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLS board filled with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print(' ' + ' '.join(COL_LABELS))
    # Print each row
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))  # bottom border

def is_valid_column(board, col_index):
    # Check if a column is within bounds and not full
    if 0 <= col_index < COLS and board[0][col_index] == ' ':
        return True
    return False

def get_next_open_row(board, col_index):
    # Returns the bottommost empty row index in the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    # If top row has no spaces, it's a draw (board full)
    return all(board[0][c] != ' ' for c in range(COLS))

def get_player_input(board, player_token):
    while True:
        choice = input(f"Player {player_token}, choose a column (A-G): ").strip().upper()
        if choice in COL_LABELS:
            col = COL_LABELS.index(choice)
            if is_valid_column(board, col):
                return col
            else:
                print("That column is full. Try another one.")
        else:
            print("Invalid input. Please enter a letter from A to G.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    board = create_board()
    players = PLAYERS_TOKENS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        player_token = players[current_player_index]
        col = get_player_input(board, player_token)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player_token)

        if winning_move(board, player_token):
            clear_screen()
            print_board(board)
            print(f"Player {player_token} wins! Congratulations!")
            game_over = True
        elif is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more valid moves.")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
