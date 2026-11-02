import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = '  ' + '   '.join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(row) + '+')

def validate_input(input_str, board):
    if len(input_str) != 1 or not input_str.isalpha():
        return False
    col = ord(input_str.upper()) - 65
    return 0 <= col < len(board[0]) and board[0][col] == ' '

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if (col <= COLS - 4 and all(board[row][c] == checker for c in range(col, col + 4)) or
                row <= ROWS - 4 and all(board[r][col] == checker for r in range(row, row + 4)) or
                row <= ROWS - 4 and col <= COLS - 4 and all(board[row + d][col + d] == checker for d in range(4)) or
                row >= 3 and col <= COLS - 4 and all(board[row - d][col + d] == checker for d in range(4))):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        if not validate_input(user_input, board):
            print("Invalid input, try again.")
            continue

        col = ord(user_input) - 65
        place_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
