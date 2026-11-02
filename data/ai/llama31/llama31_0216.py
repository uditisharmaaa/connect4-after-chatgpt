import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        print()
    print('+---' * BOARD_COLS + '+')

def is_valid_input(input_str):
    if len(input_str)!= 1:
        return False
    if not input_str.isalpha():
        return False
    if input_str.upper() < 'A' or input_str.upper() > chr(65 + BOARD_COLS - 1):
        return False
    return True

def get_column_index(input_str):
    return ord(input_str.upper()) - 65

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, player_checker, col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_checker
            return

def check_win(board, player_checker):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row][col + 1] == player_checker and board[row][col + 2] == player_checker and board[row][col + 3] == player_checker:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player_checker and board[row + 1][col] == player_checker and board[row + 2][col] == player_checker and board[row + 3][col] == player_checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row + 1][col + 1] == player_checker and board[row + 2][col + 2] == player_checker and board[row + 3][col + 3] == player_checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row - 1][col + 1] == player_checker and board[row - 2][col + 2] == player_checker and board[row - 3][col + 3] == player_checker:
                return True
    return False

def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    num_players = 2
    players_checkers = PLAYERS_CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {players_checkers[current_player_index]}, please enter a column:")
        input_str = input().strip()
        if not is_valid_input(input_str):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = get_column_index(input_str)
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        make_move(board, players_checkers[current_player_index], col)
        if check_win(board, players_checkers[current_player_index]):
            os.system('clear')
            print_board(board)
            print(f"Player {players_checkers[current_player_index]} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
