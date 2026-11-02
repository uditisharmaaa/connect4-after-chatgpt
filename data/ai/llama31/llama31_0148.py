import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with the given dimensions"""
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board, cols):
    """Print the board with column labels"""
    print('  ' + ' '.join(chr(65 + i) for i in range(cols)))
    print('+' + '+---' * cols + '+')
    for row in board:
        print('|' + '|'.join(['   ' + cell + '   ' for cell in row]) + '|')
        print('+' + '+---' * cols + '+')

def get_player_checker(players):
    """Get the checkers for the given number of players"""
    return CHECKERS[:players]

def get_random_first_player(players):
    """Randomly select the first player"""
    return random.randint(0, players - 1)

def is_valid_input(input_str, cols):
    """Check if the input is a valid column label"""
    return input_str.upper() in [chr(65 + i) for i in range(cols)]

def get_column_from_input(input_str, cols):
    """Get the column index from the input string"""
    return ord(input_str.upper()) - 65

def is_valid_move(board, col):
    """Check if the move is valid (column is not full)"""
    return board[0][col] == ' '

def make_move(board, player_checker, col):
    """Make a move by placing the checker in the lowest available space"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_checker
            return

def check_win(board, player_checker):
    """Check if the player has won"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == player_checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == player_checker for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == player_checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == player_checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)"""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def play_game():
    num_players = 2
    player_checkers = get_player_checker(num_players)
    first_player = get_random_first_player(num_players)
    board = create_board(BOARD_ROWS, BOARD_COLS)

    while True:
        os.system('clear')
        print_board(board, BOARD_COLS)
        player = (first_player + num_players - 1) % num_players
        print(f"Player {player_checkers[player]}, please enter a column:")
        input_str = input()
        while not is_valid_input(input_str, BOARD_COLS):
            print("Invalid input. Please enter a column label.")
            input_str = input()
        col = get_column_from_input(input_str, BOARD_COLS)
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        make_move(board, player_checkers[player], col)
        if check_win(board, player_checkers[player]):
            print_board(board, BOARD_COLS)
            print(f"Player {player_checkers[player]} won!")
            break
        if check_draw(board):
            print_board(board, BOARD_COLS)
            print("It's a draw!")
            break
        first_player = (first_player + 1) % num_players

play_game()
