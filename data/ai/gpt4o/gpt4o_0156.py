import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system("clear")
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(input_str, cols):
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    col_index = ord(input_str.upper()) - ord('A')
    if col_index < 0 or col_index >= cols:
        return False
    return True

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        while True:
            user_input = input().strip().upper()
            if not is_valid_input(user_input, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col_index = ord(user_input) - ord('A')
            if not place_checker(board, col_index, current_checker):
                print("Column is full. Choose another column.")
                continue
            break

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
