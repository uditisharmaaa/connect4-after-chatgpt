import os
import random
import string

# Constant variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty Connect 4 board with the given dimensions."""
    return [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """Print the current state of the Connect 4 board."""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_WIDTH]))
    print('+---' * BOARD_WIDTH + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_WIDTH + '+')

def validate_input(column, board):
    """Validate user input to ensure it's a valid column."""
    try:
        column = string.ascii_uppercase.index(column)
        if column < 0 or column >= BOARD_WIDTH:
            return False
        return True
    except ValueError:
        return False

def get_next_open_row(board, column):
    """Get the next open row in the specified column."""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    row = get_next_open_row(board, column)
    if row!= -1:
        board[row][column] = checker
        return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    """Play a game of Connect 4."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()
        while not validate_input(column, board):
            print("Invalid input. Please enter a valid column.")
            column = input().upper()
        column = string.ascii_uppercase.index(column)
        if not drop_checker(board, column, current_player):
            print("Column is full. Please try again.")
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
    game()
