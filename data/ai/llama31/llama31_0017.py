import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with whitespaces."""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def validate_input(column):
    """Check if the input is a valid column letter."""
    if len(column)!= 1 or not 'A' <= column <= 'G':
        return False
    return True

def get_next_open_row(board, column):
    """Get the next open row in a column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][ord(column) - ord('A')] == ' ':
            return row

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    row = get_next_open_row(board, column)
    if row is not None:
        board[row][ord(column) - ord('A')] = checker
        return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
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

def check_draw(board):
    """Check if the game is a draw."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()

        if not validate_input(column):
            print("Invalid input. Please enter a column letter.")
            continue

        if not place_checker(board, column, current_player):
            print("Column is full. Please choose another column.")
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
