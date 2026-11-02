import os
import random
import string

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespaces"""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    if len(input_str)!= 1 or input_str not in string.ascii_uppercase[:BOARD_COLS]:
        return False
    return True

def get_player_move(player):
    """Get the column move from the player"""
    while True:
        move = input(f"Player {player}, please enter a column: ")
        if is_valid_input(move):
            return move
        print("Invalid input. Please enter a column letter (A-G).")

def place_checker(board, player, col):
    """Place the player's checker in the specified column"""
    col_idx = string.ascii_uppercase.index(col)
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return
    print("Column is full. Please choose another column.")
    return False

def check_win(board, player):
    """Check for a win in all directions (horizontal, vertical, diagonal)"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == player for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if all([board[row][col] == player for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all([board[row+i][col+i] == player for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all([board[row-i][col+i] == player for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the board is full and no player has won"""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def game():
    """Play the Connect 4 game"""
    num_players = 2
    players = CHECKERS[:num_players]
    random.shuffle(players)
    board = create_board()
    current_player_idx = 0
    while True:
        print_board(board)
        player = players[current_player_idx]
        move = get_player_move(player)
        if place_checker(board, player, move):
            if check_win(board, player):
                print_board(board)
                print(f"Player {player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player_idx = (current_player_idx + 1) % num_players

game()
