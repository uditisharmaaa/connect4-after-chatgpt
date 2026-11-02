import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
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

def is_valid_column(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(col_letter) != 1:
        return False
    if col_letter not in letters[:COLS]:
        return False
    return True

def get_col_index(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(col_letter)

def place_checker(board, col, checker):
    # place checker in lowest empty space
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # column full

def check_win(board, checker):
    # check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and 
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True
    # check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == checker and board[r+1][c] == checker and 
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True
    # check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and 
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and 
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
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
    current = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        player = players[current]
        print(f"Player {player}, please enter a column:")
        col_input = input().strip().upper()
        if not is_valid_column(col_input):
            continue
        col = get_col_index(col_input)
        row_placed = place_checker(board, col, player)
        if row_placed == -1:
            # column full, lose turn
            current = (current +1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
