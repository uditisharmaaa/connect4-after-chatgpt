import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the specified number of rows and columns"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board, player_turn):
    """Print the current state of the board"""
    os.system('clear')
    print('  A', 'B', 'C', 'D', 'E', 'F', 'G', sep='   ')
    for i, row in enumerate(board, start=1):
        print('+---' * NUM_COLS + '+')
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        print()
    print('+---' * NUM_COLS + '+')
    print(f"Player {CHECKERS[player_turn]}, please enter a column:")

def is_valid_input(input_str, board):
    """Check if the input is a valid column letter"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    col_index = ord(input_str.upper()) - ord('A')
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    for row in reversed(board):
        if row[col_index] == ' ':
            return True
    return False

def get_player_input(board, player_turn):
    """Get the player's input and validate it"""
    while True:
        input_str = input().strip()
        if is_valid_input(input_str, board):
            return ord(input_str.upper()) - ord('A')
        print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col_index, player_checker):
    """Drop the player's checker into the specified column"""
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player_checker
            break

def check_win(board, player_checker):
    """Check if the player has won"""
    # Check horizontal locations for win
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS):
            if board[r][c] == player_checker and board[r][c+1] == player_checker and board[r][c+2] == player_checker and board[r][c+3] == player_checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS-3):
            if board[r][c] == player_checker and board[r+1][c] == player_checker and board[r+2][c] == player_checker and board[r+3][c] == player_checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS-3):
            if board[r][c] == player_checker and board[r+1][c+1] == player_checker and board[r+2][c+2] == player_checker and board[r+3][c+3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == player_checker and board[r-1][c+1] == player_checker and board[r-2][c+2] == player_checker and board[r-3][c+3] == player_checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    num_players = 2
    board = create_board()
    players = CHECKERS[:num_players]
    player_turn = random.randint(0, num_players-1)

    while True:
        print_board(board, player_turn)
        col_index = get_player_input(board, player_turn)
        drop_checker(board, col_index, players[player_turn])
        if check_win(board, players[player_turn]):
            print_board(board, player_turn)
            print(f"Player {players[player_turn]} won!")
            break
        if check_draw(board):
            print_board(board, player_turn)
            print("It's a draw!")
            break
        player_turn = (player_turn + 1) % num_players

if __name__ == "__main__":
    main()
