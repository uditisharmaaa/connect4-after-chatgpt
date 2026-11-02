import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change this for the number of players (2 to 5)

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Use 'cls' instead if you're on Windows
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (COLUMNS * 2 + 1))

def is_valid_column(board, col):
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_win(board, piece):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical check
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Positive diagonal check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Negative diagonal check
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def main():
    board = initialize_board()
    game_over = False
    turn = 0
    players = random.sample(PLAYER_SYMBOLS[:NUM_PLAYERS], NUM_PLAYERS)

    while not game_over:
        print_board(board)
        player = players[turn]

        try:
            col_input = input(f"Player {player}, choose a column (A-G): ").strip().upper()
            if col_input not in COLUMN_LABELS:
                raise ValueError
            col = COLUMN_LABELS.index(col_input)

            if not is_valid_column(board, col):
                print("Column is full! Try a different column.")
                continue
        except (ValueError, IndexError):
            print("Invalid column! Please choose a column from A to G.")
            continue

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw.")
            game_over = True
        else:
            turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
