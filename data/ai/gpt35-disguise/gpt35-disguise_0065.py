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
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # print column letters
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---"*COLS + "+")

def valid_column(col):
    if len(col) != 1:
        return False
    if not col.isalpha():
        return False
    col = col.upper()
    if ord(col) < ord('A') or ord(col) >= ord('A')+COLS:
        return False
    return True

def col_to_index(col):
    return ord(col.upper()) - ord('A')

def place_checker(board, col_i, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col_i] == " ":
            board[row][col_i] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # Horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Diagonal right down \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Diagonal left down /
    for r in range(ROWS-3):
        for c in range(3, COLS):
            if (board[r][c] == checker and
                board[r+1][c-1] == checker and
                board[r+2][c-2] == checker and
                board[r+3][c-3] == checker):
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

    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        player = players[current]
        print("Player {}, please enter a column:".format(player))
        inp = input().strip()
        while not valid_column(inp):
            print("Invalid input. Player {}, please enter a column:".format(player))
            inp = input().strip()
        col_i = col_to_index(inp)
        if not place_checker(board, col_i, player):
            print("Column full. Player {} loses turn.".format(player))
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, player):
            print("Player {} won!".format(player))
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
