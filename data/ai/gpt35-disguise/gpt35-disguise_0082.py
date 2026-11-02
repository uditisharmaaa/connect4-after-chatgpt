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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    top = "  "
    for i in range(COLS):
        top += "  " + letters[i] + " "
    print(top)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---" * COLS + "+")

def check_input(inp, board):
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    col = ord(inp) - ord('A')
    if col < 0 or col >= COLS:
        return False
    # Check if column is full
    if board[0][col] != " ":
        # Column full
        return False
    return True

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # Should not reach here if input is valid (but if full, turn is lost)
    return -1, -1

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS -3):
            if board[r][c]==checker and board[r][c+1]==checker and board[r][c+2]==checker and board[r][c+3]==checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS -3):
            if board[r][c]==checker and board[r+1][c]==checker and board[r+2][c]==checker and board[r+3][c]==checker:
                return True
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if board[r][c]==checker and board[r+1][c+1]==checker and board[r+2][c+2]==checker and board[r+3][c+3]==checker:
                return True
    # diagonal down-left
    for r in range(ROWS -3):
        for c in range(3, COLS):
            if board[r][c]==checker and board[r+1][c-1]==checker and board[r+2][c-2]==checker and board[r+3][c-3]==checker:
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
    current = random.randint(0, PLAYERS-1)
    game_over = False

    print_board(board)

    while not game_over:
        checker = players[current]
        print("Player " + checker + ", please enter a column:")
        inp = input("").strip().upper()
        if not check_input(inp, board):
            # invalid input, ask again without losing turn
            continue
        col = ord(inp) - ord('A')
        row, col = place_checker(board, col, checker)
        if row == -1:
            # Column full, turn lost
            current = (current + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
            break

        if check_draw(board):
            print("Game is a draw!")
            game_over = True
            break

        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
