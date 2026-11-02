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
        row = [" "] * COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def get_valid_columns(board):
    valid = []
    for c in range(COLS):
        if board[0][c] == " ":
            valid.append(c)
    return valid

def input_to_col(s):
    s = s.strip()
    if len(s) != 1:
        return -1
    c = ord(s.upper()) - ord('A')
    if c < 0 or c >= COLS:
        return -1
    return c

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
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
    current_player = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print("Player " + checker + ", please enter a column:")
        col_input = input()
        col = input_to_col(col_input)
        if col == -1:
            continue  # invalid input, ask again
        if board[0][col] != " ":
            # column full, player loses turn
            current_player = (current_player + 1) % PLAYERS
            continue
        placed = place_checker(board, col, checker)
        if not placed:
            # shouldn't reach here but just in case
            current_player = (current_player + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
