import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system("clear")

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for c in range(COLS):
        header += " " + letters[c] + "  "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        rowline = "|"
        for c in range(COLS):
            rowline += " " + board[r][c] + " |"
        print(rowline)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def valid_column(col, board):
    if len(col) != 1:
        return False
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col = col.upper()
    if col not in letters[:COLS]:
        return False
    col_index = letters.index(col)
    # check if column is not full
    if board[0][col_index] != " ":
        return False
    return True

def place_checker(col, board, checker):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col = col.upper()
    c = letters.index(col)
    # place checker at lowest empty row in col
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c
    return -1, -1  # column full (should not happen if checked before)

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == checker and board[r+1][c] == checker and
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # diagonal up-right
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
    current = random.randint(0, PLAYERS -1)
    print_board(board)
    
    while True:
        checker = players[current]
        valid_input = False
        while not valid_input:
            print("Player " + checker + ", please enter a column:")
            col = input()
            if valid_column(col, board):
                valid_input = True
            else:
                # If column is full (top cell taken) player loses turn
                letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if len(col) == 1 and col.upper() in letters[:COLS]:
                    c = letters.index(col.upper())
                    if board[0][c] != " ":
                        print("Column full, you lose your turn.")
                        break
                print("Invalid input, try again.")
        else:
            row, col_index = place_checker(col, board, checker)
            print_board(board)
            if check_win(board, checker):
                print("Player " + checker + " won!")
                break
            if check_draw(board):
                print("Game is a draw!")
                break
            current = (current +1) % PLAYERS
            continue
        current = (current +1) % PLAYERS
        print_board(board)


if __name__ == "__main__":
    main()
