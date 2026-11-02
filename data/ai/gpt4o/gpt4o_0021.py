import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ["X", "O"]
MAX_PLAYERS = 2

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)])
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def check_winner(board, player_symbol):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if check_direction(board, r, c, 0, 1, player_symbol) or \
               check_direction(board, r, c, 1, 0, player_symbol) or \
               check_direction(board, r, c, 1, 1, player_symbol) or \
               check_direction(board, r, c, -1, 1, player_symbol):
                return True
    return False

def check_direction(board, row, col, row_step, col_step, player_symbol):
    count = 0
    for i in range(4):
        r = row + i * row_step
        c = col + i * col_step
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            count += 1
        else:
            break
    return count == 4

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, MAX_PLAYERS - 1)
    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        col = input(f"Player {current_symbol}, please enter a column: ").upper()
        if col < 'A' or col > chr(ord('A') + COLUMNS - 1):
            print("Invalid input, try again.")
            continue
        col_index = ord(col) - ord('A')

        row = get_next_open_row(board, col_index)
        if row is None:
            print("Column full, try again.")
            continue

        board[row][col_index] = current_symbol
        print_board(board)

        if check_winner(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
