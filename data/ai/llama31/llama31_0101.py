import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players_turn):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    print('+' + '+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '+---' * BOARD_COLS + '+')
    print(f"Player {players_turn}, please enter a column:")

def validate_input(input_str, board):
    """Check if the user input is valid"""
    if not input_str.isalpha() or len(input_str)!= 1:
        return False
    col_idx = ord(input_str.upper()) - ord('A')
    if col_idx < 0 or col_idx >= BOARD_COLS:
        return False
    if board[0][col_idx]!= ' ':
        return False
    return True

def place_checker(board, col_idx, checker):
    """Place a checker at the specified column"""
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal locations for win
    for row_idx in range(BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == checker and board[row_idx][col_idx + 1] == checker and board[row_idx][col_idx + 2] == checker and board[row_idx][col_idx + 3] == checker:
                return True

    # Check vertical locations for win
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS):
            if board[row_idx][col_idx] == checker and board[row_idx + 1][col_idx] == checker and board[row_idx + 2][col_idx] == checker and board[row_idx + 3][col_idx] == checker:
                return True

    # Check positively sloped diagonals
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == checker and board[row_idx + 1][col_idx + 1] == checker and board[row_idx + 2][col_idx + 2] == checker and board[row_idx + 3][col_idx + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row_idx in range(3, BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == checker and board[row_idx - 1][col_idx + 1] == checker and board[row_idx - 2][col_idx + 2] == checker and board[row_idx - 3][col_idx + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row_idx in range(BOARD_ROWS):
        for col_idx in range(BOARD_COLS):
            if board[row_idx][col_idx] == ' ':
                return False
    return True

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board()
    current_player_idx = random.randint(0, num_players - 1)

    while True:
        print_board(board, players[current_player_idx])
        input_str = input().upper()
        if not validate_input(input_str, board):
            print("Invalid input. Please try again.")
            continue
        col_idx = ord(input_str) - ord('A')
        place_checker(board, col_idx, players[current_player_idx])
        if check_win(board, players[current_player_idx]):
            print_board(board, players[current_player_idx])
            print(f"Player {players[current_player_idx]} won!")
            break
        if check_draw(board):
            print_board(board, players[current_player_idx])
            print("It's a draw!")
            break
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
