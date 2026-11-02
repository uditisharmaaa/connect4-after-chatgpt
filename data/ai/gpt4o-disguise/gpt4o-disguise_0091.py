import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_EMPTY = " "

def create_board():
    return [[BOARD_EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")
    
def get_valid_column(board):
    valid_input = False
    while not valid_input:
        column = input(f"Player {player_token}, please enter a column: ").strip().upper()
        if len(column) == 1 and ord('A') <= ord(column) < ord('A') + COLS:
            col_num = ord(column) - ord('A')
            if board[0][col_num] == BOARD_EMPTY:
                valid_input = True
            else:
                print("Column is full! Try another one.")
        else:
            print("Invalid input! Please enter a valid column.")
    return col_num

def place_checker(board, col, player_token):
    for row in reversed(board):
        if row[col] == BOARD_EMPTY:
            row[col] = player_token
            break

def check_win(board, player_token):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player_token:
                # Check horizontal
                if col <= COLS - 4 and all(board[row][c] == player_token for c in range(col, col + 4)):
                    return True
                # Check vertical
                if row <= ROWS - 4 and all(board[r][col] == player_token for r in range(row, row + 4)):
                    return True
                # Check diagonal /
                if row <= ROWS - 4 and col >= 3 and all(board[row + i][col - i] == player_token for i in range(4)):
                    return True
                # Check diagonal \
                if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == player_token for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][col] != BOARD_EMPTY for col in range(COLS))

board = create_board()
player_tokens = CHECKERS[:NUM_PLAYERS]
current_player_idx = random.choice(range(NUM_PLAYERS))

while True:
    print_board(board)
    player_token = player_tokens[current_player_idx]
    col = get_valid_column(board)
    place_checker(board, col, player_token)
    if check_win(board, player_token):
        print_board(board)
        print(f"Player {player_token} won!")
        break
    if check_draw(board):
        print_board(board)
        print("The game is a draw!")
        break
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
