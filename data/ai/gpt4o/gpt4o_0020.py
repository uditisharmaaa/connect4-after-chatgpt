import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players
COLUMN_NAMES = [chr(i) for i in range(65, 65 + COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = '  ' + '   '.join(COLUMN_NAMES[:len(board[0])])
    print(header)
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+---' * len(row) + '+')

def check_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def check_winner(board, player_checker):
    rows, columns = len(board), len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Check diagonal (bottom left to top right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    return False

def validate_input(input_str, board):
    if input_str in COLUMN_NAMES[:len(board[0])]:
        col_idx = COLUMN_NAMES.index(input_str)
        if any(cell == ' ' for cell in [board[row][col_idx] for row in range(len(board))]):
            return col_idx
    return None

def place_checker(board, column, player_checker):
    for row in reversed(range(len(board))):
        if board[row][column] == ' ':
            board[row][column] = player_checker
            return True
    return False

def connect_4_game():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYER_COUNT]
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)

    while True:
        current_player_checker = players[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        while True:
            user_input = input("Column: ").strip().upper()
            column_index = validate_input(user_input, board)
            if column_index is not None:
                break
            print("Invalid input! Please enter a valid column.")

        if place_checker(board, column_index, current_player_checker):
            print_board(board)
            if check_winner(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                break
            if check_board_full(board):
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % PLAYER_COUNT
        else:
            print("Column is full. Turn is lost.")

if __name__ == "__main__":
    connect_4_game()
