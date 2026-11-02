import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels and player's checkers."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_input(column):
    """Check if the user input is a valid column label."""
    return column.upper() >= 'A' and column.upper() <= chr(ord('A') + BOARD_COLS - 1)

def get_player_checker(player_num):
    """Get the checker symbol for a given player number."""
    return CHECKERS[player_num - 1]

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check for a win condition in the board."""
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

    return False

def is_draw(board):
    """Check if the board is full (draw condition)."""
    return all(cell!= ' ' for row in board for cell in row)

def play_game():
    """Play the Connect 4 game."""
    board = create_board()
    players = 2
    checkers = CHECKERS[:players]
    current_player = random.randint(1, players)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")
        column = input().strip()

        if not is_valid_input(column):
            print("Invalid input. Please try again.")
            continue

        column = ord(column.upper()) - ord('A')

        if all(cell!= ' ' for cell in [row[column] for row in board]):
            print("Column is full. Please try again.")
            continue

        drop_checker(board, column, get_player_checker(current_player))

        if check_win(board, get_player_checker(current_player)):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break

        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player % players) + 1

play_game()
