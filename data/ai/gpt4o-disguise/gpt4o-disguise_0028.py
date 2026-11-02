import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    print("  " + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + ' | '.join(row) + " |")
    print("+---" * COLS + "+")

def random_player():
    return random.randint(0, PLAYERS - 1)

def get_column_input():
    while True:
        col = input(f"Player {checkers[current_player]}, please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1):
            return ord(col) - 65
        else:
            print("Invalid input. Please enter a valid column!")

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board):
    def check_sequence(seq):
        for i in range(len(seq) - 3):
            if seq[i] == seq[i+1] == seq[i+2] == seq[i+3] != ' ':
                return True
        return False

    for row in range(ROWS):
        if check_sequence(board[row]): return True

    for col in range(COLS):
        if check_sequence([board[row][col] for row in range(ROWS)]): return True

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] != ' ':
                return True
            if board[row+3][col] == board[row+2][col+1] == board[row+1][col+2] == board[row][col+3] != ' ':
                return True

    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

board = create_board(ROWS, COLS)
checkers = CHECKERS[:PLAYERS]
current_player = random_player()

clear_screen()
print_board(board)

while True:
    col = get_column_input()
    if not place_checker(board, col, checkers[current_player]):
        print("Column is full! Player loses turn.")
    else:
        clear_screen()
        print_board(board)
        if check_win(board):
            print(f"Player {checkers[current_player]} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS
