import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
EMPTY = " "
WIN_CONDITION = 4
COLUMN_LETTERS = [chr(i) for i in range(ord("A"), ord("A") + COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    
    print("  " + "   ".join(COLUMN_LETTERS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(board, col):
    return col in COLUMN_LETTERS and board[0][COLUMN_LETTERS.index(col)] == EMPTY

def make_move(board, col, checker):
    col_idx = COLUMN_LETTERS.index(col)
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == EMPTY:
            board[row][col_idx] = checker
            break

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(WIN_CONDITION)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != EMPTY for col in range(COLS))

def main():
    board = create_board()
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        move = input().strip().upper()

        if not is_valid_move(board, move):
            print("Invalid move! Try again.")
            continue

        make_move(board, move, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
