import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Creates a 2D board with all elements initialized with whitespaces.
    """
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """
    Prints the current state of the board.
    """
    os.system('clear')
    print('  A', 'B', 'C', 'D', 'E', 'F', 'G', sep='   ')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|', end='')
        for cell in row:
            print(' ' + cell + ' |', end='')
        print()
    print('+---' * BOARD_COLS + '+')

def is_valid_move(board, col):
    """
    Checks if a move is valid (i.e., the column is not full).
    """
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """
    Returns the next open row in the given column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

def drop_piece(board, row, col, piece):
    """
    Drops a piece into the given column.
    """
    board[row][col] = piece

def winning_move(board, piece):
    """
    Checks for a winning move.
    """
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_game(board):
    """
    Checks if the game is a draw.
    """
    return ' ' not in [cell for row in board for cell in row]

def game():
    """
    Runs the Connect 4 game.
    """
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{chr(64 + BOARD_COLS)}):")
        col_choice = input().upper()

        # Validate input
        while col_choice not in [chr(i) for i in range(65, 65 + BOARD_COLS)]:
            print("Invalid input. Please enter a column letter.")
            col_choice = input().upper()

        col = ord(col_choice) - 65

        # Validate move
        while not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            col_choice = input().upper()
            col = ord(col_choice) - 65

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_player)

        # Check for win
        if winning_move(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check for draw
        if draw_game(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch players
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

game()
