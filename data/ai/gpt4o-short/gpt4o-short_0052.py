import random
import os

# Constants to define the game settings
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players
NUM_PLAYERS = 3  # Change this to set the number of players
COLUMN_LABELS = 'ABCDEFG'  # Labels for the columns

def clear_screen():
    os.system('clear')  # Use 'cls' on Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print each row
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLUMNS + 1))

def get_valid_columns(board):
    return [c for c in range(COLUMNS) if board[0][c] == ' ']

def drop_piece(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            break

def validate_input(column, valid_columns):
    return column in valid_columns

def check_winner(board, player_symbol):
    # Horizontal, vertical, and diagonal checks
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == player_symbol for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == player_symbol for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == player_symbol for i in range(4)):
                return True
            if all(board[r+3-i][c+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect4():
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    while True:
        print_board(board)
        print(f"Player {player_symbols[current_player_idx]}'s turn")

        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("It's a draw!")
            break

        # Get and validate player input
        while True:
            move = input(f"Choose a column ({COLUMN_LABELS}): ").upper()
            if move in COLUMN_LABELS:
                column = COLUMN_LABELS.index(move)
                if validate_input(column, valid_columns):
                    break
            print("Invalid move. Try again.")

        # Drop the piece in the chosen column
        drop_piece(board, column, player_symbols[current_player_idx])

        # Check for a win or draw
        if check_winner(board, player_symbols[current_player_idx]):
            print_board(board)
            print(f"Player {player_symbols[current_player_idx]} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    connect4()
