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
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_line = "|"
        for c in range(COLS):
            row_line += " " + board[r][c] + " |"
        print(row_line)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def valid_input(inp):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp >= chr(ord('A') + COLS):
        return False
    return True

def place_checker(board, col, checker):
    # col is index 0-based
    # put checker in lowest empty row in that col
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_index = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        player = players[current_index]
        inp = input("Player " + player + ", please enter a column: ")
        inp = inp.strip().upper()
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        placed = place_checker(board, col, player)
        if not placed:
            # column full, player loses turn
            current_index = (current_index + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, player):
            print("Player " + player + " won!")
            break
        if board_full(board):
            print("Draw!")
            break
        current_index = (current_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
