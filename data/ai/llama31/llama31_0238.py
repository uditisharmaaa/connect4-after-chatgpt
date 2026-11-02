import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespaces"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print('  A B C D E F G')
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|', end='')
        for cell in row:
            print(' ' + cell + ' |', end='')
        print()
    print('+---' * NUM_COLS + '+')

def get_player_checker(player_num):
    """Return the checker for the given player number"""
    return CHECKERS[player_num - 1]

def get_next_player(current_player):
    """Return the next player number"""
    return (current_player % NUM_PLAYERS) + 1

def is_valid_move(board, col):
    """Check if a move is valid (i.e., the column is not full)"""
    return board[0][col] == ' '

def get_lowest_available_row(board, col):
    """Return the lowest available row in the given column"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def make_move(board, player_num, col):
    """Make a move on the board"""
    row = get_lowest_available_row(board, col)
    if row!= -1:
        board[row][col] = get_player_checker(player_num)
    return row!= -1

def check_win(board, player_num):
    """Check if the given player has won"""
    checker = get_player_checker(player_num)

    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (i.e., the board is full)"""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(1, NUM_PLAYERS)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")
        while True:
            col_input = input().upper()
            if col_input >= 'A' and col_input <= 'G':
                col = ord(col_input) - ord('A')
                if is_valid_move(board, col):
                    break
                else:
                    print("Column is full, please try again.")
            else:
                print("Invalid input, please try again.")
        make_move(board, current_player, col)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
