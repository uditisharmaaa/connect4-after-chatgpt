import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with whitespaces"""
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board, cols):
    """Print the board with column labels"""
    print('  ' + '   '.join(chr(65 + i) for i in range(cols)))
    print('+---' + '+---' * (cols - 1))
    for row in board:
        print('|   ' + '|   '.join(row) + '|')
        print('+---' + '+---' * (cols - 1))

def get_valid_input(player, cols):
    """Get a valid column input from the player"""
    while True:
        col = input(f"Player {CHECKERS[player]}, please enter a column: ")
        if col.upper() >= 'A' and col.upper() <= chr(65 + cols - 1):
            return ord(col.upper()) - 65
        print("Invalid input. Please enter a column letter.")

def place_checker(board, player, col):
    """Place a checker in the lowest available space in the column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = CHECKERS[player]
            return

def check_win(board, player):
    """Check for a win in all directions"""
    checker = CHECKERS[player]
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the board is full"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the Connect 4 game"""
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0
    while True:
        os.system('clear')
        print_board(board, BOARD_COLS)
        col = get_valid_input(players[current_player], BOARD_COLS)
        place_checker(board, players[current_player], col)
        if check_win(board, players[current_player]):
            os.system('clear')
            print_board(board, BOARD_COLS)
            print(f"Player {CHECKERS[players[current_player]]} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board, BOARD_COLS)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

game()
