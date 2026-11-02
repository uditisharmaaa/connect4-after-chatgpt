import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespace"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(BOARD_COLS)))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def get_player_checker(player):
    """Get the checker symbol for a given player"""
    return CHECKERS[player - 1]

def is_valid_input(column):
    """Check if the input column is valid"""
    return 'A' <= column <= chr(65 + BOARD_COLS - 1)

def is_valid_move(board, column):
    """Check if a move is valid (i.e., column is not full)"""
    return board[0][ord(column) - 65] == ' '

def make_move(board, player, column):
    """Make a move by placing a checker in the given column"""
    checker = get_player_checker(player)
    for row in reversed(board):
        if row[ord(column) - 65] == ' ':
            row[ord(column) - 65] = checker
            break

def check_win(board, player):
    """Check if the given player has won"""
    checker = get_player_checker(player)
    # Check horizontal wins
    for row in board:
        for i in range(BOARD_COLS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True
    # Check vertical wins
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (i.e., the board is full)"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the Connect 4 game"""
    board = create_board()
    player = random.randint(1, NUM_PLAYERS)
    print_board(board)
    while True:
        column = input(f"Player {get_player_checker(player)}, please enter a column: ").upper()
        if not is_valid_input(column):
            print("Invalid input. Please try again.")
            continue
        if not is_valid_move(board, column):
            print("Column is full. Please try again.")
            continue
        make_move(board, player, column)
        print_board(board)
        if check_win(board, player):
            print(f"Player {get_player_checker(player)} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        player = (player % NUM_PLAYERS) + 1

if __name__ == "__main__":
    game()
