import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def is_valid_input(input_char, columns):
    if len(input_char) == 1 and 'A' <= input_char <= chr(ord('A') + columns - 1):
        return True
    return False

def check_win(board, checker):
    def check_line(line):
        return any(line[i] == checker and line[i:i+4] == [checker] * 4 for i in range(len(line) - 3))

    # Check horizontal
    for row in board:
        if check_line(row):
            return True

    # Check vertical
    for col in range(COLUMNS):
        column_checkers = [board[row][col] for row in range(ROWS)]
        if check_line(column_checkers):
            return True

    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = initialize_board(ROWS, COLUMNS)
    turn = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        current_checker = CHECKERS[turn]
        print(f"Player {current_checker}, please enter a column:")
        col_input = input().strip().upper()

        if not is_valid_input(col_input, COLUMNS):
            print("Invalid input! Please enter a valid column letter.")
            continue

        col = ord(col_input) - ord('A')
        row = get_next_open_row(board, col)

        if row is None:
            print("Column is full! You lost your turn.")
        else:
            board[row][col] = current_checker

            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        turn = (turn + 1) % PLAYERS
        print_board(board)

if __name__ == "__main__":
    main()
