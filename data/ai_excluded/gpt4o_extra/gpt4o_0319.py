import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col):
    return col.isalpha() and ord(col.upper()) - ord('A') < COLS

def get_available_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col_input = input().strip()

        if not is_valid_input(col_input):
            print("Invalid input. Please try again.")
            continue

        col = ord(col_input.upper()) - ord('A')
        row = get_available_row(board, col)

        if row is None:
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % PLAYERS
        else:
            board[row][col] = CHECKERS[current_player]
            print_board(board)

            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if check_for_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
