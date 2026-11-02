import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 4  # Change this from 2 to 5 as needed

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('   '.join(COLUMN_LABELS))
    for row in board:
        print(' | '.join(row))
        print('-' * (COLS * 4 - 1))

def drop_piece(board, col, symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return True
    return False

def is_valid_column(choice):
    return choice in COLUMN_LABELS

def get_column_index(choice):
    return COLUMN_LABELS.index(choice)

def is_winning_move(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect4():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    game_over = False

    while not game_over:
        print_board(board)
        current_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {current_symbol}, it's your turn. Make your move!")

        choice = input("Choose a column (A-G): ").strip().upper()
        if not is_valid_column(choice):
            print("Invalid column! Please choose a valid column (A-G).")
            input("Press Enter to continue...")
            continue

        col_index = get_column_index(choice)
        if not drop_piece(board, col_index, current_symbol):
            print("Column full! Please choose another column.")
            input("Press Enter to continue...")
            continue

        if is_winning_move(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4()
