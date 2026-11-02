import os
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2

def create_board():
    return [[' ' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def print_board(board):
    os.system('clear')
    header = '   '.join([chr(65 + i) for i in range(COLUMN_COUNT)])
    print('  ' + header)
    print('+---' * COLUMN_COUNT + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMN_COUNT + '+')

def is_valid_move(board, col):
    return 0 <= col < COLUMN_COUNT and board[0][col] == ' '

def make_move(board, col, checker):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            break

def check_win(board, checker):
    # Check horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check diagonal /
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check diagonal \
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMN_COUNT))

def play_game():
    board = create_board()
    num_players = 2  # Between 2 and 5
    checkers = ['X', 'O', 'V', 'H', 'M'][:num_players]
    current_player = random.randint(0, num_players - 1)

    print_board(board)
    
    while True:
        print(f"Player {checkers[current_player]}, please enter a column:")
        column_input = input().upper()
        col = ord(column_input) - 65
        
        if not is_valid_move(board, col):
            print("Invalid move. Try again.")
            continue

        make_move(board, col, checkers[current_player])
        print_board(board)

        if check_win(board, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

play_game()
