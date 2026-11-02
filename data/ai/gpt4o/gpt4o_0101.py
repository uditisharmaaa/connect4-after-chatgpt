import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:MAX_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    col_labels = '   '.join(chr(65 + i) for i in range(len(board[0])))
    border = '+---' * len(board[0]) + '+'
    print(f"  {col_labels}")
    for row in board:
        print(border)
        print("| " + " | ".join(row) + " |")
    print(border)

def valid_input(input_char, cols):
    return len(input_char) == 1 and input_char.isalpha() and ('A' <= input_char <= chr(65 + cols - 1))

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_winner(board, checker, streak):
    # Check horizontal, vertical, and diagonal for wins
    def consecutive_count(lst):
        count = max_count = 0
        for item in lst:
            count = count + 1 if item == checker else 0
            max_count = max(max_count, count)
        return max_count >= streak

    for row in board:
        if consecutive_count(row):
            return True

    for col_idx in range(len(board[0])):
        if consecutive_count([board[row_idx][col_idx] for row_idx in range(len(board))]):
            return True

    diagonals = []
    for di in range(-len(board) + 1, len(board[0])):
        diagonals.append([board[r][r + di] for r in range(len(board)) if 0 <= r + di < len(board[0])])
    diagonals += [[board[r][c] for r in range(len(board)) for c in range(len(board[0]))
                   if r - c == di] for di in range(len(board[0]) + len(board) - 1)]

    for diag in diagonals:
        if len(diag) >= streak and consecutive_count(diag):
            return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect_4_game():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, MAX_PLAYERS - 1)
    streak_to_win = 4

    while True:
        print_board(board)
        current_checker = CHECKERS[current_player_idx]
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        if not valid_input(user_input, COLS):
            print("Invalid input, try again.")
            continue

        column = ord(user_input) - 65

        if place_checker(board, column, current_checker):
            if check_winner(board, current_checker, streak_to_win):
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player_idx = (current_player_idx + 1) % MAX_PLAYERS
        else:
            print(f"Column {user_input} is full, try another one.")

connect_4_game()
