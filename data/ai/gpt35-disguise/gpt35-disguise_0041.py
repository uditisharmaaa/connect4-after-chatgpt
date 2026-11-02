import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        rowline = "|"
        for c in range(COLS):
            rowline += " " + board[r][c] + " |"
        print(rowline)
    print(line)

def valid_column(ch):
    if len(ch) != 1:
        return False
    col = ord(ch) - ord('A')
    if col < 0 or col >= COLS:
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_horizontal(board, r, c, checker):
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_vertical(board, r, c, checker):
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_diagonal(board, r, c, checker):
    # Check /
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c < COLS - 1:
        start_r -= 1
        start_c += 1
    while start_r < ROWS and start_c >= 0:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r += 1
        start_c -= 1
    # Check \
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    while start_r < ROWS and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r += 1
        start_c += 1
    return False

def check_win(board, r, c, checker):
    return check_horizontal(board, r, c, checker) or check_vertical(board, r, c, checker) or check_diagonal(board, r, c, checker)

def check_draw(board):
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
        player = players[current_player]
        while True:
            print("Player {}, please enter a column:".format(player))
            col_input = input()
            if not valid_column(col_input):
                continue
            col = ord(col_input) - ord('A')
            if column_full(board, col):
                # Player loses turn if column is full
                break
            else:
                r, c = place_checker(board, col, player)
                break
        print_board(board)
        if not column_full(board, col):
            if check_win(board, r, c, player):
                print("Player {} won!".format(player))
                break
            if check_draw(board):
                print("Game is a draw.")
                break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
