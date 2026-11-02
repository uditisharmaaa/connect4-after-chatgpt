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
        row = [" "] * COLS
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for c in range(COLS):
        print(" " + letters[c] + "  ", end="")
    print()
    line = "+---" * COLS + "+"
    for r in range(ROWS):
        print(line)
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print(line)

def get_valid_column(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) != 1 or col not in letters[:COLS]:
            continue
        col_idx = letters.index(col)
        if board[0][col_idx] != " ":
            # column full, lose turn
            return -1
        return col_idx

def place_checker(board, col, checker):
    for r in range(ROWS -1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS -3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal down-left
    for r in range(ROWS -3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS -1)
    players = CHECKERS[:PLAYERS]
    print_board(board)

    while True:
        checker = players[current_player_index]
        col = get_valid_column(checker, board)
        if col == -1:
            # lose turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        place_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
