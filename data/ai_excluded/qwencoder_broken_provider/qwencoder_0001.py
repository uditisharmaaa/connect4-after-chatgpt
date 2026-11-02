import os
import random

# Constants
ROWS = 6
COLS =7PLAYERS = ['X', 'O']
EMPTY = ' '

def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)) + "  ")
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(cell for cell in row) + " |")
        print("+" + "---+" * COLS)

def get_player_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column) == 1 and 'A' <= column <= chr(64 + COLS):
            col_index = ord(column) - 65
            if board[0][col_index] == EMPTY:
                return col_index
            else:
                print("Column is full, please choose another one.")
        else:
            print("Invalid input, please try again.")

def drop_checker(board, col_index, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = player
            return row, col_index

def check_win(board, last_row, last_col, player):
    # Check horizontal
    count = 0
    for col in range(max(0, last_col - 3), min(COLS, last_col + 4)):
        count = count + 1 if board[last_row][col] == player else 0    if count == 4:
            return True

    # Check vertical
    count = 0
    for row in range(max(0, last_row - 3), min(ROWS, last_row + 4)):
        count = count + 1 if board[row][last_col] == player else 0    if count == 4:
            return True

    # Check diagonal (bottom-left to top-right)
    count = 0
    for offset in range(-3,4):
        r, c = last_row + offset, last_col - offset
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    for offset in range(-3,4):
        r, c = last_row + offset, last_col + offset
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    return False

def check_draw(board):
    return all(board[0][col] != EMPTY for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col_index = get_player_input(current_player)
        last_row, last_col = drop_checker(board, col_index, current_player)
        print_board(board)

        if check_win(board, last_row, last_col, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
