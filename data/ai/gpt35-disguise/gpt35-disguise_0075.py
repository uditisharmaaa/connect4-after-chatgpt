import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = [chr(ord("A") + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_col(col_str):
    if len(col_str) != 1:
        return False
    c = col_str.upper()
    if c < "A" or c >= chr(ord("A") + COLS):
        return False
    return True

def col_to_index(c):
    return ord(c.upper()) - ord("A")

def drop_checker(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_horizontal(board, r, c, checker):
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_vertical(board, r, c, checker):
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_diagonal(board, r, c, checker):
    # Check / diagonal
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c < COLS - 1:
        start_r -= 1
        start_c += 1
    row = start_r
    col = start_c
    while row < ROWS and col >= 0:
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row += 1
        col -= 1

    # Check \ diagonal
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    row = start_r
    col = start_c
    while row < ROWS and col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row += 1
        col += 1

    return False

def check_win(board, r, c, checker):
    if check_horizontal(board, r, c, checker):
        return True
    if check_vertical(board, r, c, checker):
        return True
    if check_diagonal(board, r, c, checker):
        return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        player_checker = players[current_player]
        print("Player {}, please enter a column:".format(player_checker))
        col_input = input().strip()
        if not is_valid_col(col_input):
            # invalid input, ask again, turn not lost
            continue
        col_index = col_to_index(col_input)
        row_index = drop_checker(board, col_index, player_checker)
        if row_index == -1:
            # column full, lose turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, row_index, col_index, player_checker):
            print("Player {} won!".format(player_checker))
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
