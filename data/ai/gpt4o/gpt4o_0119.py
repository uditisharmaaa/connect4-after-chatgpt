import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def check_win(board, last_row, last_col, symbol):
    # Check horizontal
    for col in range(COLUMNS - 3):
        if board[last_row][col:col + 4] == [symbol] * 4:
            return True

    # Check vertical
    if last_row <= ROWS - 4:
        if all(board[last_row + i][last_col] == symbol for i in range(4)):
            return True
    
    # Check diagonals
    for r_offset, c_offset in [(-3, -3), (-3, 3), (3, 3), (3, -3)]:
        for i in range(4):
            row_start = last_row + r_offset + i
            col_start = last_col + c_offset + i
            if 0 <= row_start < ROWS - 3 and 0 <= col_start < COLUMNS - 3:
                if all(board[row_start + j][col_start + j * (-1 if c_offset < 0 else 1)] == symbol for j in range(4)):
                    return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def make_move(board, player_symbol):
    while True:
        column = input(f"Player {player_symbol}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(64 + COLUMNS):
            col_index = ord(column) - 65
            if board[0][col_index] == " ":
                for row_index in range(ROWS - 1, -1, -1):
                    if board[row_index][col_index] == " ":
                        board[row_index][col_index] = player_symbol
                        return row_index, col_index
            else:
                print("Column is full. You lose your turn.")
                return None, None
        else:
            print("Invalid input. Please use letters A-G.")

def connect4():
    board = create_board(ROWS, COLUMNS)

    # Set game parameters
    num_players = MIN_PLAYERS
    player_symbols = CHECKER_SYMBOLS[:num_players]

    current_player_index = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        last_row, last_col = make_move(board, player_symbols[current_player_index])
        print_board(board)

        if last_row is not None and last_col is not None:
            if check_win(board, last_row, last_col, player_symbols[current_player_index]):
                print(f"Player {player_symbols[current_player_index]} won!")
                break

        if check_draw(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    connect4()
