import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_LEN = 4
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
    # print column letters
    letters = ""
    for i in range(COLS):
        letters += "  " + chr(ord('A') + i) + " "
    print(letters)
    # print rows and separators
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_line = "|"
        for c in range(COLS):
            row_line += " " + board[r][c] + " |"
        print(row_line)
    print(line)

def input_column(player):
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not col.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        col = col.upper()
        c_num = ord(col) - ord('A')
        if c_num < 0 or c_num >= COLS:
            print("Invalid column. Please enter a letter within the board.")
            continue
        return c_num

def place_checker(board, col, checker):
    # place checker in the lowest empty spot in the column
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LEN:
                    return True
            else:
                count = 0
    # vertical check
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count +=1
                if count == WIN_LEN:
                    return True
            else:
                count = 0
    # diagonal (\) check
    for r in range(ROWS - WIN_LEN + 1):
        for c in range(COLS - WIN_LEN + 1):
            count = 0
            for i in range(WIN_LEN):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LEN:
                return True
    # diagonal (/) check
    for r in range(WIN_LEN -1, ROWS):
        for c in range(COLS - WIN_LEN + 1):
            count = 0
            for i in range(WIN_LEN):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LEN:
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

board = create_board()
current_player = random.randint(0, PLAYERS -1)
players_checkers = CHECKERS[:PLAYERS]

print_board(board)

while True:
    player_checker = players_checkers[current_player]
    col = input_column(player_checker)
    placed = place_checker(board, col, player_checker)
    if not placed:
        # column full, lose turn
        print("Column is full. Turn lost.")
    else:
        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
    print_board(board)
    current_player = (current_player +1) % PLAYERS
