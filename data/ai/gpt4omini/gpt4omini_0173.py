import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+".join([""] * COLS) + "-+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join([""] * COLS) + "-+")

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= 'G':
            col_index = ord(column) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full. Try again.")
        else:
            print("Invalid input. Please enter a letter between A and G.")

def drop_checker(board, col_index, player):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            return row, col_index
    return None

def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if (check_direction(board, r, c, 0, 1, player) or  # Horizontal
                    check_direction(board, r, c, 1, 0, player) or  # Vertical
                    check_direction(board, r, c, 1, 1, player) or  # Diagonal /
                    check_direction(board, r, c, 1, -1, player)):  # Diagonal \
                    return True
    return False

def check_direction(board, start_row, start_col, delta_row, delta_col, player):
    count = 0
    for i in range(4):
        r = start_row + i * delta_row
        c = start_col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game logic
board = create_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col_index = get_valid_input(current_player)
    drop_checker(board, col_index, current_player)
    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        break
    if is_draw(board):
        print("The game is a draw!")
        break

    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
