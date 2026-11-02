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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for c in range(COLS):
        header += " " + letters[c] + "  "
    print(header)
    line = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def check_input(inp, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(inp) != 1:
        return False
    if inp not in letters[:COLS]:
        return False
    col = letters.index(inp)
    if board[0][col] != " ":
        # column full
        return "full"
    return True

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None

def is_winner(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal \
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    i = 0
    while start_r + i < ROWS and start_c + i < COLS:
        if board[start_r + i][start_c + i] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        i += 1
    # diagonal /
    count = 0
    start_r = r
    start_c = c
    while start_r < ROWS - 1 and start_c > 0:
        start_r += 1
        start_c -= 1
    i = 0
    while start_r - i >= 0 and start_c + i < COLS:
        if board[start_r - i][start_c + i] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        i += 1
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        player = players[current]
        inp = input("Player {}, please enter a column: ".format(player))
        inp = inp.upper()
        valid = check_input(inp, board)
        if valid == False:
            # invalid input
            continue
        if valid == "full":
            # lose turn
            current = (current +1) % PLAYERS
            continue
        col = ord(inp) - ord("A")
        r, c = place_checker(board, col, player)
        print_board(board)

        if is_winner(board, r, c, player):
            print("Player {} won!".format(player))
            break
        if is_draw(board):
            print("Game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
