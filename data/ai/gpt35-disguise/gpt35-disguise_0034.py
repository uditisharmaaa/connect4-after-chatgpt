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
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
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
        print("+---"*COLS + "+")
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+---"*COLS + "+")

def is_valid_column(col):
    if len(col) != 1:
        return False
    c = col[0]
    if not ('A' <= c <= chr(ord('A') + COLS -1)):
        return False
    return True

def get_col_index(col):
    return ord(col) - ord('A')

def place_checker(board, col, checker):
    c = col
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r
    return -1

def is_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS -3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS -3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS -3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        checker = players[current]
        print("Player " + checker + ", please enter a column:")
        valid_input = False
        while not valid_input:
            col_input = input()
            if not is_valid_column(col_input):
                print("Invalid column. Please enter a valid column:")
                continue
            col_index = get_col_index(col_input)
            if col_index <0 or col_index >= COLS:
                print("Invalid column. Please enter a valid column:")
                continue
            # check if column full
            if board[0][col_index] != " ":
                # lose turn
                print("Column full, you lose your turn.")
                break
            valid_input = True
        if valid_input:
            row_placed = place_checker(board, col_index, checker)
            print_board(board)
            if is_win(board, checker):
                print("Player " + checker + " won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
