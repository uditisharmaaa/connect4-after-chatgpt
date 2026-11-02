import os
import random
import string

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checker symbols for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Create a 2D board with the specified dimensions.
    """
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """
    Print the current state of the board.
    """
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS)

def validate_input(input_str):
    """
    Validate the user's input to ensure it's a valid column letter.
    """
    if len(input_str)!= 1 or input_str not in string.ascii_uppercase[:BOARD_COLS]:
        return False
    return True

def get_next_open_row(board, col):
    """
    Find the next available row in the specified column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def drop_checker(board, col, checker):
    """
    Drop the checker into the specified column.
    """
    row = get_next_open_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def check_win(board, checker):
    """
    Check if the specified player has won.
    """
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

def check_draw(board):
    """
    Check if the game has ended in a draw.
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    """
    Main game loop.
    """
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{string.ascii_uppercase[BOARD_COLS-1]}):")
        input_str = input().upper()
        while not validate_input(input_str):
            print("Invalid input. Please try again.")
            input_str = input().upper()

        col = ord(input_str) - ord('A')
        if not drop_checker(board, col, current_player):
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

        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    game()
