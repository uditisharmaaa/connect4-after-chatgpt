import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4

CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+"*COLS)

def valid_input(inp, board):
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    col = ord(inp.upper()) - ord('A')
    if col < 0 or col >= COLS:
        return False
    # check if column is full
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # column full

def check_winner(board, checker, row, col):
    # horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count +=1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count +=1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    # diagonal top-left to bottom-right
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    count = 0
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count +=1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1
    # diagonal bottom-left to top-right
    start_row = row
    start_col = col
    while start_row < ROWS-1 and start_col > 0:
        start_row += 1
        start_col -= 1
    count = 0
    while start_row >= 0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = CHECKERS[current_player]
        print("Player " + checker + ", please enter a column:")
        inp = input()
        if not valid_input(inp, board):
            # lost turn if column full, else ask again
            col = ord(inp.upper()) - ord('A') if len(inp)==1 and inp.isalpha() else -1
            if 0 <= col < COLS and board[0][col] != " ":
                # column full -> lose turn
                current_player = (current_player + 1) % PLAYERS
                print_board(board)
                continue
            # invalid input ask again
            continue
        col = ord(inp.upper()) - ord('A')
        pos = place_checker(board, col, checker)
        if pos is None:
            # column full, lose turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        row, col = pos
        print_board(board)
        if check_winner(board, checker, row, col):
            print("Player " + checker + " won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
