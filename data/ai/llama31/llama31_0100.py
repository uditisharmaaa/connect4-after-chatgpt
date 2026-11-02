import os
import random
import string

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with given dimensions"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def validate_input(col, board):
    """Check if the user input is valid"""
    if not col.isalpha():
        return False
    if not 'A' <= col <= 'G':
        return False
    col_index = ord(col) - ord('A')
    if board[0][col_index]!= ' ':
        return False
    return True

def place_checker(col, player, board):
    """Place the checker at the correct location"""
    col_index = ord(col) - ord('A')
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = player
            return

def check_win(board):
    """Check if there is a winner"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3]!= ' ':
                return row[i]
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col]!= ' ':
                return board[i][col]
    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]!= ' ':
                return board[row][col]
            if board[row][col + 3] == board[row + 1][col + 2] == board[row + 2][col + 1] == board[row + 3][col]!= ' ':
                return board[row][col + 3]
    return None

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Main game loop"""
    board = create_board()
    players = CHECKERS[:random.randint(MIN_PLAYERS, MAX_PLAYERS)]
    random.shuffle(players)
    current_player_index = 0

    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}, please enter a column:")
        col = input().upper()
        while not validate_input(col, board):
            print("Invalid input, please try again:")
            col = input().upper()
        place_checker(col, players[current_player_index], board)
        winner = check_win(board)
        if winner:
            print_board(board)
            print(f"Player {winner} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % len(players)

game()
