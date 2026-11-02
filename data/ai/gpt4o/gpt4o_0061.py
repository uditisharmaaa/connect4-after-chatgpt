import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i + 65) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def check_win(board, player_symbol):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_direction(board, row, col, player_symbol, 1, 0) or
                check_direction(board, row, col, player_symbol, 0, 1) or
                check_direction(board, row, col, player_symbol, 1, 1) or
                check_direction(board, row, col, player_symbol, 1, -1)):
                return True
    return False

def check_direction(board, row, col, player_symbol, d_row, d_col):
    for i in range(4):
        r, c = row + i * d_row, col + i * d_col
        if r >= ROWS or c >= COLUMNS or r < 0 or c < 0 or board[r][c] != player_symbol:
            return False
    return True

def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def drop_checker(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player_symbol
            return True
    return False

def is_valid_input(input_str):
    return len(input_str) == 1 and ord(input_str.upper()) in range(65, 65 + COLUMNS)

def play_game():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    print_board(board)
    
    while True:
        print(f"Player {player_symbols[current_player]}, please enter a column:")
        user_input = input().upper()

        if not is_valid_input(user_input):
            print("Invalid input. Try again.")
            continue
        
        column = ord(user_input) - 65
        
        if not drop_checker(board, column, player_symbols[current_player]):
            print("Column full or invalid. Turn lost.")
        else:
            print_board(board)
            if check_win(board, player_symbols[current_player]):
                print(f"Player {player_symbols[current_player]} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
