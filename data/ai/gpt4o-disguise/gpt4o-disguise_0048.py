import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Only first PLAYERS checkers will be used

def print_board(board):
    os.system('clear')
    print("  " + "   ".join("ABCDEFG"[:COLS]))
    for row in board:
        print("+" + "---+" * COLS)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * COLS)

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def is_valid_input(x):
    return x.isalpha() and x in "ABCDEFG"[:COLS]

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def has_won(board, checker):
    # Check Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
                
    # Check Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    
    # Check Diagonal /
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True

    # Check Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
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
    active_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        current_checker = CHECKERS[active_player]
        valid_input = False

        while not valid_input:
            col_input = input(f'Player {current_checker}, please enter a column: ').upper()
            if not is_valid_input(col_input):
                print("Invalid input. Please enter a column letter A-G.")
                continue
            col = ord(col_input) - ord('A')
            row = get_next_open_row(board, col)
            if row == -1:
                print("Column full. Please choose another column.")
            else:
                valid_input = True

        board[row][col] = current_checker
        print_board(board)

        if has_won(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        active_player = (active_player + 1) % PLAYERS

main()
