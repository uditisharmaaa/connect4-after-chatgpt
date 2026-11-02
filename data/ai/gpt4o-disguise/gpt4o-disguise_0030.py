import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = 2

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(choice, board):
    if choice.isalpha() and len(choice) == 1:
        col = ord(choice.upper()) - 65
        if 0 <= col < len(board[0]) and board[0][col] == " ":
            return True
    return False

def make_move(board, choice, checker):
    col = ord(choice.upper()) - 65
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if all(row[col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]

    print_board(board)
    while True:
        print(f"Player {checkers[current_player]}, please enter a column:")
        choice = input().strip()
        if is_valid_column(choice, board):
            make_move(board, choice, checkers[current_player])
            print_board(board)
            
            if check_win(board, checkers[current_player]):
                print(f"Player {checkers[current_player]} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Invalid input, try again.")

if __name__ == "__main__":
    main()
