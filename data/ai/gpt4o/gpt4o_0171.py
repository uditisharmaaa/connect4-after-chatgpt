import os
import random

# Global Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def init_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)])
    separator = "+---" * COLUMNS + "+"

    print(header)
    for row in board:
        print(separator)
        print('| ' + ' | '.join(row) + ' |')
    print(separator)

def get_valid_input():
    while True:
        player_input = input().upper()
        if len(player_input) == 1 and 'A' <= player_input < chr(ord('A') + COLUMNS):
            return player_input
        else:
            print("Invalid input. Please enter a column (A-G).")

def place_checker(board, column, symbol):
    col_idx = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = symbol
            return True
    print("Column full. You lose your turn.")
    return False

def check_for_win(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[c] == symbol for c in range(col, col + 4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[r][col] == symbol for r in range(row, row + 4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = init_board()
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        symbol = player_symbols[current_player]
        print(f"Player {symbol}, please enter a column:")
        column = get_valid_input()
        
        if place_checker(board, column, symbol):
            print_board(board)
            if check_for_win(board, symbol):
                print(f"Player {symbol} won!")
                break
            elif check_for_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
