import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen for Linux/Unix terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

def get_empty_row(board, column):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1

def check_winner(board, player):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                if check_direction(board, row, col, player, 1, 0) or \
                   check_direction(board, row, col, player, 0, 1) or \
                   check_direction(board, row, col, player, 1, 1) or \
                   check_direction(board, row, col, player, 1, -1):
                    return True
    return False

def check_direction(board, row, col, player, d_row, d_col):
    count = 0
    for _ in range(4):
        if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
            count += 1
        else:
            break
        row += d_row
        col += d_col
    return count == 4

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if not is_valid_input(column):
            continue
        col_index = ord(column) - 65
        row_index = get_empty_row(board, col_index)
        
        if row_index == -1:
            continue
        
        board[row_index][col_index] = current_player
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            return
        if is_draw(board):
            print("The game is a draw!")
            return
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
