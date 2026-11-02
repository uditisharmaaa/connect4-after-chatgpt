import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(c) for c in range(ord('A'), ord('A') + COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_column(column, board):
    return 0 <= column < COLS and board[0][column] == " "

def get_column_input():
    while True:
        try:
            user_input = input("Please enter a column (A-G): ").strip()
            column = ord(user_input.upper()) - ord('A')
            if column >= 0 and column < COLS:
                return column
        except (ValueError, TypeError):
            pass
        print("Invalid input. Try again.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    # Horizontal, Vertical, Diagonal checks
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r+i][c-i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board(ROWS, COLS)
    current_player = random.choice(range(PLAYERS))
    checkers = CHECKERS[:PLAYERS]

    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, it's your turn.")
        column = get_column_input()
        
        if is_valid_column(column, board):
            place_checker(board, column, checkers[current_player])
            if check_win(board, checkers[current_player]):
                print_board(board)
                print(f"Player {checkers[current_player]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. You lose your turn.")

play_game()
