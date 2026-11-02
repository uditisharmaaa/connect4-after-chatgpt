import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    col_labels = '  '.join([chr(ord('A') + i) for i in range(COLUMNS)])
    print('  ' + col_labels)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_input(input_char):
    return ord('A') <= ord(input_char) < ord('A') + COLUMNS

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == ' ':
            return r
    return None

def check_for_win(board, checker):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all([board[r][c+i] == checker for i in range(4)]):
                return True
    # Check vertical locations
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all([board[r+i][c] == checker for i in range(4)]):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all([board[r+i][c+i] == checker for i in range(4)]):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all([board[r-i][c+i] == checker for i in range(4)]):
                return True
    return False

def check_for_draw(board):
    return all(board[r][c] != ' ' for r in range(ROWS) for c in range(COLUMNS))

def connect_4():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    game_active = True

    print_board(board)

    while game_active:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        player_input = input().strip().upper()
        if not is_valid_input(player_input):
            print("Invalid input. Try again.")
            continue

        col = ord(player_input) - ord('A')
        row = get_next_open_row(board, col)
        if row is None:
            print("Column is full. You lose the turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        board[row][col] = current_checker

        if check_for_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_active = False
        elif check_for_draw(board):
            print_board(board)
            print("It's a draw!")
            game_active = False
        else:
            print_board(board)
            current_player_index = (current_player_index + 1) % PLAYERS

connect_4()
