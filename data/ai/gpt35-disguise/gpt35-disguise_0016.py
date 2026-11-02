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
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---" * COLS + "+")

def valid_input(s):
    if len(s) != 1:
        return False
    if s < 'A' or s >= chr(ord('A') + COLS):
        return False
    return True

def place_checker(board, col, checker):
    # col is index 0 based
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Diagonal check down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Diagonal check up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
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
    current = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        player = players[current]
        print("Player {}, please enter a column:".format(player))
        move = input().strip().upper()

        if not valid_input(move):
            print("Invalid input. Try again.")
            continue

        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print("Invalid column. Try again.")
            continue

        placed = place_checker(board, col, player)
        if not placed:
            print("Column full, you lose your turn.")
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
