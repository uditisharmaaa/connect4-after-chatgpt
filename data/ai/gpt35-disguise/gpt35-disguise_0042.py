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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    top = "  "
    for c in range(COLS):
        top += " " + letters[c] + "  "
    print(top)
    line = "+---"*COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def check_input(inp):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(inp) != 1:
        return False
    up = inp.upper()
    if up not in letters[:COLS]:
        return False
    return True

def get_column_index(letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(letter.upper())

def place_checker(board, col, checker):
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
                count +=1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical check
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count +=1
                if count ==4:
                    return True
            else:
                count=0
    # diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right check
    for r in range(3, ROWS):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
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
    current_player = random.randint(0, PLAYERS-1)
    while True:
        clear_screen()
        print_board(board)
        print("Player " + players[current_player] + ", please enter a column:")
        inp = input()
        while not check_input(inp):
            print("Invalid input. Please enter a column letter between A and " + chr(ord('A')+COLS-1) + ":")
            inp = input()
        col = get_column_index(inp)
        placed = place_checker(board, col, players[current_player])
        if not placed:
            # lose turn
            current_player = (current_player + 1) % PLAYERS
            continue
        if check_win(board, players[current_player]):
            clear_screen()
            print_board(board)
            print("Player " + players[current_player] + " won!")
            break
        if board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
