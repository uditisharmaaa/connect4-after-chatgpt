import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  A B C D E F G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_index):
    """Get the checker for the specified player."""
    return CHECKERS[player_index]

def is_valid_input(column):
    """Check if the input column is valid."""
    return 'A' <= column <= 'G'

def is_valid_move(board, column):
    """Check if the move is valid."""
    return board[0][ord(column) - ord('A')] == ' '

def get_next_open_row(board, column):
    """Get the next open row in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][ord(column) - ord('A')] == ' ':
            return row

def drop_checker(board, row, column, checker):
    """Drop the checker in the specified column."""
    board[row][ord(column) - ord('A')] = checker

def check_for_win(board, checker):
    """Check if there is a win."""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def play_game():
    """Play the Connect 4 game."""
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0
    turn = 0

    while True:
        os.system('clear')
        print_board(board)
        current_player = players[current_player_index]
        print("Player {}, please enter a column:".format(get_player_checker(current_player)))
        column = input().upper()

        if not is_valid_input(column):
            print("Invalid input. Please enter a letter between A and G.")
            continue

        if not is_valid_move(board, column):
            print("Invalid move. Column is full.")
            continue

        row = get_next_open_row(board, column)
        drop_checker(board, row, column, get_player_checker(current_player))

        if check_for_win(board, get_player_checker(current_player)):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(get_player_checker(current_player)))
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        turn += 1

        # Check for a draw
        if turn == BOARD_ROWS * BOARD_COLS:
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

play_game()
