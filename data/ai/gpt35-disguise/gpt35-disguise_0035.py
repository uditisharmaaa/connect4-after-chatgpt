import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    cols_label = "  "
    for i in range(COLS):
        cols_label += chr(ord('A') + i) + "   "
    print(cols_label)
    line = "+" + "---+" * COLS
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + COLS - 1)):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # diagonal /
    count = 0
    start_row = row
    start_col = col
    while start_row > 0 and start_col < COLS -1:
        start_row -=1
        start_col +=1
    r = start_row
    c = start_col
    count = 0
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c -= 1

    # diagonal \
    count = 0
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -=1
        start_col -=1
    r = start_row
    c = start_col
    count = 0
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    player_order = list(range(PLAYERS))
    current_player_index = random.choice(player_order)
    clear()
    print_board(board)
    while True:
        player = player_order[current_player_index]
        checker = CHECKERS[player]
        print("Player {}, please enter a column:".format(checker))
        while True:
            col_input = input().strip().upper()
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = get_column_index(col_input)
            row_placed = place_checker(board, col, checker)
            if row_placed == -1:
                print("Column full, turn lost.")
                break
            else:
                break

        clear()
        print_board(board)

        if row_placed != -1:
            if check_win(board, row_placed, col, checker):
                print("Player {} won!".format(checker))
                break
            if board_full(board):
                print("The game is a draw.")
                break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
