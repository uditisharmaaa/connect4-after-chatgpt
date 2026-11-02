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
        board.append([" "]*COLS)
    return board

def print_board(board):
    letters = [chr(i) for i in range(ord("A"), ord("A")+COLS)]
    print(" ", end=" ")
    for l in letters:
        print(l, end="   ")
    print()
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
        print("+---"*COLS + "+")

def get_valid_column(board, player):
    letters = [chr(i) for i in range(ord("A"), ord("A")+COLS)]
    while True:
        print(f"Player {player}, please enter a column:")
        col = input().strip().upper()
        if len(col) != 1 or col not in letters:
            continue
        c = ord(col) - ord("A")
        # check if column is full
        if board[0][c] != " ":
            # loses turn
            return -1
        return c

def place_checker(board, col, checker):
    # place checker in lowest empty spot in the column
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # Check vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and 
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and 
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        clear_screen()
        print_board(board)
        col = get_valid_column(board, current_player)
        if col == -1:
            # column full, player loses turn
            # just switch player
            i = players.index(current_player)
            current_player = players[(i+1)%PLAYERS]
            continue
        place_checker(board, col, current_player)
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        i = players.index(current_player)
        current_player = players[(i+1)%PLAYERS]

if __name__ == "__main__":
    main()
