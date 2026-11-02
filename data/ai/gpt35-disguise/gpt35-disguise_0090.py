import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column(ch):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if ch in letters[:COLS]:
        return True
    return False

def get_column(ch):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(ch)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
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
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # diagonal /
    for r in range(WIN_COUNT-1, ROWS):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # diagonal \
    for r in range(ROWS - WIN_COUNT +1):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
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
    players = []
    for i in range(PLAYERS):
        players.append(CHECKERS[i])
    current = random.randint(0, PLAYERS-1)

    print_board(board)
    while True:
        checker = players[current]
        print("Player " + checker + ", please enter a column:")
        inp = input().strip().upper()

        if not is_valid_column(inp):
            continue

        col = get_column(inp)
        if not place_checker(board, col, checker):
            # Column full, lose turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
