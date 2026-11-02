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
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear()
    header = "  "
    for c in range(COLS):
        header += chr(ord('A')+c) + "   "
    print(header)
    for r in range(ROWS):
        print('+' + "---+"*COLS)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print('+' + "---+"*COLS)

def choose_player():
    return random.randint(0, PLAYERS-1)

def valid_input(s):
    if len(s) != 1:
        return False
    c = s[0]
    if c < 'A' or c >= chr(ord('A') + COLS):
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(max(0, c-3), min(COLS, c+4)):
        if board[r][col] == checker:
            count +=1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(max(0, r-3), min(ROWS, r+4)):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    start_row = r + min(3, COLS-1 - c, r)
    start_col = c - min(3, COLS-1 - c, r)
    while start_row >= 0 and start_col < COLS:
        rr = start_row
        cc = start_col
        count = 0
        while rr < ROWS and cc < COLS:
            if board[rr][cc] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            rr += 1
            cc += 1
        start_row -= 1
        start_col += 1
    # diagonal \
    count = 0
    start_row = r - min(3, r, c)
    start_col = c - min(3, r, c)
    while start_row < ROWS and start_col < COLS:
        rr = start_row
        cc = start_col
        count = 0
        while rr < ROWS and cc >= 0:
            if board[rr][cc] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            rr += 1
            cc -= 1
        start_row += 1
        start_col += 1
    return False

def full_board(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    current_player = choose_player()
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print("Player " + checker + ", please enter a column:")
        col_in = input().strip().upper()

        if not valid_input(col_in):
            continue
        col = ord(col_in) - ord('A')
        if col < 0 or col >= COLS:
            continue
        if column_full(board, col):
            # player loses turn
            current_player = (current_player +1) % PLAYERS
            continue

        row = place_checker(board, col, checker)
        print_board(board)

        if check_win(board, row, col, checker):
            print("Player " + checker + " won!")
            break

        if full_board(board):
            print("Draw!")
            break
        current_player = (current_player +1) % PLAYERS

if __name__ == "__main__":
    main()
