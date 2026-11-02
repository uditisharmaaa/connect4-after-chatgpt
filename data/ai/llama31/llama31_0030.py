import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Create an empty 2D board with the specified dimensions.
    """
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """
    Print the current state of the board.
    """
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for i in range(BOARD_ROWS):
        print('+---' * BOARD_COLS + '+')
        row = '|'
        for j in range(BOARD_COLS):
            row += ' ' + board[i][j] + ' |'
        print(row)
    print('+---' * BOARD_COLS + '+')

def validate_input(column):
    """
    Validate the user input (column).
    """
    if not column.isalpha():
        return False
    column = ord(column.upper()) - 65
    if column < 0 or column >= BOARD_COLS:
        return False
    return True

def place_checker(board, column, checker):
    """
    Place the checker in the specified column.
    """
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = checker
            return

def check_win(board, checker):
    """
    Check for a win (horizontally, vertically, diagonally).
    """
    # Check horizontal
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS - 3):
            if board[i][j] == checker and board[i][j + 1] == checker and board[i][j + 2] == checker and board[i][j + 3] == checker:
                return True

    # Check vertical
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLS):
            if board[i][j] == checker and board[i + 1][j] == checker and board[i + 2][j] == checker and board[i + 3][j] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLS - 3):
            if board[i][j] == checker and board[i + 1][j + 1] == checker and board[i + 2][j + 2] == checker and board[i + 3][j + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for i in range(3, BOARD_ROWS):
        for j in range(BOARD_COLS - 3):
            if board[i][j] == checker and board[i - 1][j + 1] == checker and board[i - 2][j + 2] == checker and board[i - 3][j + 3] == checker:
                return True

    return False

def check_draw(board):
    """
    Check for a draw (board is full).
    """
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == ' ':
                return False
    return True

def game():
    """
    Main game loop.
    """
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column = input().strip()
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        column = ord(column.upper()) - 65
        if board[0][column]!= ' ':
            print("Column is full. Please choose another column.")
            continue
        place_checker(board, column, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    game()
