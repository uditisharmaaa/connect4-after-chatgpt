import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checker symbols for players
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the specified dimensions and initialize with whitespaces"""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels and row separators"""
    print('  ' + ' '.join(chr(65 + i) for i in range(BOARD_COLS)))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')

def get_player_checker(player_index):
    """Return the checker symbol for the given player index"""
    return CHECKER_SYMBOLS[player_index]

def get_next_player(current_player_index):
    """Return the index of the next player"""
    return (current_player_index + 1) % NUM_PLAYERS

def is_valid_input(column):
    """Check if the input column is valid (a letter between A and G)"""
    return 'A' <= column <= chr(65 + BOARD_COLS - 1)

def get_column_index(column):
    """Convert the input column letter to a zero-based index"""
    return ord(column) - 65

def is_column_full(board, column_index):
    """Check if the specified column is full"""
    return board[0][column_index]!= ' '

def get_next_available_row(board, column_index):
    """Return the index of the next available row in the specified column"""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index
    return -1

def place_checker(board, player_index, column_index):
    """Place the player's checker in the specified column"""
    row_index = get_next_available_row(board, column_index)
    if row_index!= -1:
        board[row_index][column_index] = get_player_checker(player_index)
        return True
    return False

def check_win(board, player_index):
    """Check if the player has won"""
    checker = get_player_checker(player_index)
    # Check horizontal wins
    for row in board:
        for i in range(BOARD_COLS - 3):
            if all(cell == checker for cell in row[i:i + 4]):
                return True
    # Check vertical wins
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i + 4)):
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)"""
    return all(cell!= ' ' for row in board for cell in row)

def game_loop():
    """Main game loop"""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        os.system('clear')
        print_board(board)
        print("Player", get_player_checker(current_player_index), "turn")
        column = input("Enter a column: ").upper()
        while not is_valid_input(column) or is_column_full(board, get_column_index(column)):
            print("Invalid input. Please try again.")
            column = input("Enter a column: ").upper()
        if not place_checker(board, current_player_index, get_column_index(column)):
            print("Column is full. Please try again.")
            continue
        if check_win(board, current_player_index):
            os.system('clear')
            print_board(board)
            print("Player", get_player_checker(current_player_index), "won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = get_next_player(current_player_index)

game_loop()
