import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system("clear")

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+---"*COLS + "+")
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+---"*COLS + "+")

def get_player_input(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        choice = input("Player " + player + ", please enter a column: ")
        if len(choice) != 1:
            continue
        choice = choice.upper()
        if choice not in letters[0:COLS]:
            continue
        col = letters.index(choice)
        if board[0][col] != " ":
            # column full
            return -1
        return col

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    # column full
    return -1

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
    # diagonal down-right
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # diagonal up-right
    for r in range(WIN_COUNT -1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r-i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    cur = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        player_checker = players[cur]
        col = get_player_input(player_checker, board)
        if col == -1:
            # column full so lose turn
            cur = (cur +1) % PLAYERS
            continue
        place_checker(board, col, player_checker)
        print_board(board)
        if check_win(board, player_checker):
            print("Player " + player_checker + " won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        cur = (cur +1) % PLAYERS

if __name__ == "__main__":
    main()
