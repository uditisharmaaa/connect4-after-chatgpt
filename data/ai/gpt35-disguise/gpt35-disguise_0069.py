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
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    header = " "
    for i in range(COLS):
        header += "  " + chr(ord('A') + i) + " "
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
    print(line)

def get_column_choice(player, board):
    while True:
        col = input("Player {}, please enter a column: ".format(player))
        if len(col) != 1:
            continue
        if not col.isalpha():
            continue
        col = col.upper()
        idx = ord(col) - ord('A')
        if idx < 0 or idx >= COLS:
            continue
        if board[0][idx] != " ":
            # top cell full means column full
            # player loses turn in that case
            return None
        return idx

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diag down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diag up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)

    print_board(board)
    while True:
        c = players[current]
        col = get_column_choice(c, board)
        if col is None:
            # lose turn
            current = (current + 1) % PLAYERS
            continue
        place_checker(board, col, c)
        print_board(board)
        if check_win(board, c):
            print("Player {} won!".format(c))
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
