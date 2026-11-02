import random
import os

# Constants
ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(i) for i in range(65, 65 + COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def is_valid_input(input_str):
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str < chr(65 + COLS)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal wins
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                for dr, dc in directions:
                    if all(0 <= row + dr * i < ROWS and 0 <= col + dc * i < COLS and board[row + dr * i][col + dc * i] == checker for i in range(4)):
                        return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col_input = input().upper()

        if not is_valid_input(col_input):
            print("Invalid input, try again.")
            continue

        col = ord(col_input) - 65

        if not drop_checker(board, col, CHECKERS[current_player]):
            print("Column full, turn lost.")
        else:
            print_board(board)
            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
