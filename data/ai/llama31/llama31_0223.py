import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespace characters"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print('  ' + ' '.join(string.ascii_uppercase[:NUM_COLS]))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * NUM_COLS + '+')

def get_player_checker(player_index):
    """Get the checker for the current player"""
    return CHECKERS[player_index % len(CHECKERS)]

def is_valid_move(board, column):
    """Check if a move is valid (i.e., column is not full)"""
    return board[NUM_ROWS - 1][column] == ' '

def get_next_open_row(board, column):
    """Get the next open row in a column"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1

def make_move(board, player_index, column):
    """Make a move on the board"""
    row = get_next_open_row(board, column)
    if row!= -1:
        board[row][column] = get_player_checker(player_index)
        return True
    return False

def check_win(board):
    """Check for a win in the current state of the board"""
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3]!= ' ':
                return True
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]!= ' ':
                return True
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3]!= ' ':
                return True
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3]!= ' ':
                return True
    return False

def check_draw(board):
    """Check for a draw in the current state of the board"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column (A-{string.ascii_uppercase[NUM_COLS - 1]}):")
        while True:
            try:
                column = input().strip().upper()
                if column not in string.ascii_uppercase[:NUM_COLS]:
                    print("Invalid input. Please enter a valid column.")
                elif not is_valid_move(board, string.ascii_uppercase.index(column)):
                    print("Column is full. Please choose another column.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid column.")
        if make_move(board, current_player, string.ascii_uppercase.index(column)):
            if check_win(board):
                os.system('clear')
                print_board(board)
                print(f"Player {get_player_checker(current_player)} won!")
                break
            elif check_draw(board):
                os.system('clear')
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    game()
