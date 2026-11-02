import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    letters = ""
    for i in range(COLS):
        letters += "  " + chr(ord('A') + i) + " "
    print(letters)
    print("+" + "---+"*COLS)
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+" + "---+"*COLS)

def is_valid_column(ch):
    if len(ch) != 1:
        return False
    if ch < 'A' or ch > chr(ord('A') + COLS - 1):
        return False
    return True

def get_column_index(ch):
    return ord(ch) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # column full

def check_line(board, r, c, dr, dc, checker):
    count = 0
    for _ in range(4):
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        if board[r][c] != checker:
            return False
        r += dr
        c += dc
    return True

def check_win(board, r, c, checker):
    # horizontal
    for start_c in range(c-3, c+1):
        if start_c < 0 or start_c + 3 >= COLS:
            continue
        if check_line(board, r, start_c, 0, 1, checker):
            return True
    # vertical
    for start_r in range(r-3, r+1):
        if start_r < 0 or start_r + 3 >= ROWS:
            continue
        if check_line(board, start_r, c, 1, 0, checker):
            return True
    # diagonal down-right
    for i in range(4):
        start_r = r - i
        start_c = c - i
        if start_r < 0 or start_r +3 >= ROWS or start_c < 0 or start_c +3 >= COLS:
            continue
        if check_line(board, start_r, start_c, 1, 1, checker):
            return True
    # diagonal up-right
    for i in range(4):
        start_r = r + i
        start_c = c - i
        if start_r >= ROWS or start_r -3 < 0 or start_c < 0 or start_c +3 >= COLS:
            continue
        if check_line(board, start_r, start_c, -1, 1, checker):
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = PLAYERS
    checkers = CHECKERS[:players]
    current_player_index = random.randint(0, players -1)
    
    print_board(board)
    
    while True:
        checker = checkers[current_player_index]
        print(f"Player {checker}, please enter a column:")
        inp = input()
        inp = inp.strip().upper()
        if not is_valid_column(inp):
            continue
        col = get_column_index(inp)
        row = place_checker(board, col, checker)
        if row == -1:
            # column full, lose turn
            current_player_index = (current_player_index +1) % players
            continue
        print_board(board)
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index +1) % players

if __name__ == "__main__":
    main()
