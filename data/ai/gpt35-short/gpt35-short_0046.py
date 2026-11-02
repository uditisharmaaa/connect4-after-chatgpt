import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')  # clear terminal screen

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' ', end=' ')
    for c in COL_LABELS:
        print(c, end=' ')
    print()
    for r in range(ROWS):
        print('|', end=' ')
        for c in range(COLS):
            print(board[r][c], end=' ')
        print('|')
    print('-' * (COLS * 2 + 3))

def get_valid_column(input_str):
    input_str = input_str.upper()
    if input_str in COL_LABELS:
        return COL_LABELS.index(input_str)
    return -1

def drop_piece(board, col, symbol):
    # Drop piece from bottom in the chosen column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col
    return -1, -1  # Column full

def check_win(board, symbol):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and 
                board[r][c+1] == symbol and
                board[r][c+2] == symbol and
                board[r][c+3] == symbol):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == symbol and
                board[r+1][c] == symbol and
                board[r+2][c] == symbol and
                board[r+3][c] == symbol):
                return True

    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r+1][c+1] == symbol and
                board[r+2][c+2] == symbol and
                board[r+3][c+3] == symbol):
                return True

    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r-1][c+1] == symbol and
                board[r-2][c+2] == symbol and
                board[r-3][c+3] == symbol):
                return True

    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == ' ':  # top row empty means not full
            return False
    return True

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    # select number of players between 2-5
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input, please enter a number.")

    players = PLAYER_SYMBOLS[:num_players]
    current_player_idx = random.randint(0, num_players -1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_symbol = players[current_player_idx]
        print(f"Player {current_symbol}'s turn.")

        col = -1
        while col == -1:
            user_input = input(f"Choose a column ({', '.join(COL_LABELS)}): ").strip().upper()
            col = get_valid_column(user_input)
            if col == -1:
                print("Invalid column. Try again.")
            elif board[0][col] != ' ':
                print("Column is full. Try another one.")
                col = -1

        row, dropped_col = drop_piece(board, col, current_symbol)
        if row == -1:
            print("Something went wrong dropping the piece.")
            continue

        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

    print("Game over. Thanks for playing!")

if __name__ == "__main__":
    main()
