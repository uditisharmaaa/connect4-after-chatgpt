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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    # Print column headers
    header = " "
    for c in range(COLS):
        header += "  " + chr(ord('A') + c) + " "
    print(header)
    # Print board rows
    for r in range(ROWS):
        line = "+"
        for _ in range(COLS):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def is_valid_col(ch):
    if len(ch) != 1:
        return False
    col = ord(ch) - ord('A')
    if col < 0 or col >= COLS:
        return False
    return True

def drop_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None, None

def check_win(board, checker, r, c):
    # check horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check diagonal /
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c < COLS-1:
        start_r -= 1
        start_c += 1
    row = start_r
    col = start_c
    count = 0
    while row < ROWS and col >= 0:
        if board[row][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        row += 1
        col -= 1
    # check diagonal \
    start_r = r
    start_c = c
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    row = start_r
    col = start_c
    count = 0
    while row < ROWS and col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        row += 1
        col += 1
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        checker = players[turn]
        valid_move = False
        print("Player " + checker + ", please enter a column:")
        user_input = input()
        while True:
            if not is_valid_col(user_input):
                print("Invalid input. Please enter a valid column letter:")
                user_input = input()
                continue
            col = ord(user_input) - ord('A')
            if board[0][col] != " ":
                # column full, turn lost
                print("Column full, you lose your turn.")
                valid_move = False
                break
            r, c = drop_checker(board, col, checker)
            if r is None:
                # Should not happen as we already checked column full
                print("Cannot place checker here.")
                user_input = input("Please enter another column:")
                continue
            valid_move = True
            break
        if valid_move:
            print_board(board)
            if check_win(board, checker, r, c):
                print("Player " + checker + " won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
