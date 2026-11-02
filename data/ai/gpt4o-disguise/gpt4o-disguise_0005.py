import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_input(input_str):
    return len(input_str) == 1 and input_str.isalpha() and input_str.upper() in COLUMN_LABELS

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().upper()

        if not is_valid_input(user_input):
            print("Invalid input. Try again.")
            continue

        col = COLUMN_LABELS.index(user_input)

        if not place_checker(board, col, CHECKERS[current_player]):
            print("Column full! You lose your turn.")
            current_player = (current_player + 1) % PLAYERS
            continue

        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

main()
