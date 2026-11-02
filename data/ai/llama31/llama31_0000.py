import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels and row separators"""
    print('  ' + ' '.join(chr(65 + i) for i in range(BOARD_COLS)))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('|   ' * BOARD_COLS + '|')
        print('+---' * BOARD_COLS + '+')
    print()

def is_valid_move(board, col):
    """Check if a move is valid (column not full)"""
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """Get the next open row in the given column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

def make_move(board, col, checker):
    """Make a move by placing the checker in the given column"""
    row = get_next_open_row(board, col)
    board[row][col] = checker

def winning_move(board, checker):
    """Check for a winning move (4 checkers in a row)"""
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

def game_over(board):
    """Check if the game is over (win or draw)"""
    for checker in CHECKERS[:2]:  # only check for 2 players
        if winning_move(board, checker):
            return True
    if all(cell!= ' ' for row in board for cell in row):
        return True
    return False

def play_game():
    """Play the Connect 4 game"""
    board = create_board()
    players = 2
    checkers = CHECKERS[:players]
    current_player = random.randint(0, players - 1)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column (A-{}):".format(chr(65 + BOARD_COLS - 1)))
        move = input().upper()
        if not move or not move.isalpha() or not 'A' <= move <= 'A' + BOARD_COLS - 1:
            print("Invalid move, try again.")
            continue
        col = ord(move) - 65
        if not is_valid_move(board, col):
            print("Column is full, try again.")
            continue
        make_move(board, col, checkers[current_player])
        if game_over(board):
            os.system('clear')
            print_board(board)
            if winning_move(board, checkers[current_player]):
                print(f"Player {checkers[current_player]} won!")
            else:
                print("It's a draw!")
            break
        current_player = (current_player + 1) % players

play_game()
