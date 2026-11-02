import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board():
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

def check_input(inp):
    if len(inp) != 1:
        return False
    c = inp[0]
    if not ('A' <= c <= chr(ord('A')+COLS-1)):
        return False
    return True

def place_checker(col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(checker):
    # horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count +=1
                if count == WIN_COUNT:
                    return True
            else:
                count =0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count +=1
                if count == WIN_COUNT:
                    return True
            else:
                count =0
    # diagonal down-right
    for r in range(ROWS - WIN_COUNT +1):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c+i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # diagonal up-right
    for r in range(WIN_COUNT -1, ROWS):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    return False

def board_full():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board()

    while True:
        print("Player {}, please enter a column:".format(players[current]))
        inp = input().strip().upper()
        if not check_input(inp):
            continue
        col = ord(inp) - ord('A')
        if col < 0 or col >= COLS:
            continue
        placed = place_checker(col, players[current])
        if not placed:
            # lose turn if full
            current = (current +1) % PLAYERS
            print_board()
            continue
        print_board()
        if check_win(players[current]):
            print("Player {} won!".format(players[current]))
            break
        if board_full():
            print("Game is a draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
