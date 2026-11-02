import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with whitespaces."""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print('   {}'.format(chr(65 + col)), end='')
    print()
    print('+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS):
        print('|', end='')
        for col in range(BOARD_COLS):
            print('   {} |'.format(board[row][col]), end='')
        print()
        print('+---' * BOARD_COLS + '+')

def get_player_checker(player_index):
    """Get the checker for the current player."""
    return CHECKERS[player_index]

def get_valid_columns(board):
    """Get a list of valid columns where a checker can be placed."""
    valid_columns = []
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            valid_columns.append(col)
    return valid_columns

def get_next_open_row(board, col):
    """Get the next open row in a given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def drop_checker(board, col, checker):
    """Drop a checker into a column."""
    row = get_next_open_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def check_win(board, checker):
    """Check if a player has won."""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_valid_input():
    """Get a valid column input from the user."""
    while True:
        col = input("Enter a column (A-{}): ".format(chr(65 + BOARD_COLS - 1)))
        if len(col)!= 1 or not col.isalpha() or not col.upper() >= 'A' or not col.upper() <= chr(65 + BOARD_COLS - 1):
            print("Invalid input. Please enter a letter between A and {}.".format(chr(65 + BOARD_COLS - 1)))
        else:
            return ord(col.upper()) - 65

def main():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0
    while True:
        print_board(board)
        player_checker = get_player_checker(players[current_player_index])
        print("Player {}, please enter a column:".format(player_checker))
        col = get_valid_input()
        valid_columns = get_valid_columns(board)
        if col not in valid_columns:
            print("Column is full. Please choose another column.")
            continue
        if not drop_checker(board, col, player_checker):
            print("Column is full. Please choose another column.")
            continue
        if check_win(board, player_checker):
            print_board(board)
            print("Player {} won!".format(player_checker))
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
