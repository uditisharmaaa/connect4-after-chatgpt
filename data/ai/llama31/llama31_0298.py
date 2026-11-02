import os
import random
import string

# Constant global variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D board with whitespace characters"""
    board = [[' ' for _ in range(width)] for _ in range(height)]
    return board

def print_board(board):
    """Print the board to the console"""
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_WIDTH]))
    print('+---' * BOARD_WIDTH + '+')
    
    # Print rows
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_WIDTH + '+')

def is_valid_input(input_str, board):
    """Check if the input is a valid column label"""
    try:
        # Convert input to uppercase and check if it's a valid column label
        col_label = input_str.upper()
        col_idx = string.ascii_uppercase.index(col_label)
        # Check if the column is not full
        return col_idx < BOARD_WIDTH and board[0][col_idx] == ' '
    except ValueError:
        return False

def place_checker(board, col_idx, checker):
    """Place a checker in the specified column"""
    for row_idx in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return

def check_win(board, checker):
    """Check if there's a win condition for the specified checker"""
    # Check horizontal wins
    for row_idx in range(BOARD_HEIGHT):
        for col_idx in range(BOARD_WIDTH - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx][col_idx + 1] == checker and \
               board[row_idx][col_idx + 2] == checker and \
               board[row_idx][col_idx + 3] == checker:
                return True
    
    # Check vertical wins
    for col_idx in range(BOARD_WIDTH):
        for row_idx in range(BOARD_HEIGHT - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx + 1][col_idx] == checker and \
               board[row_idx + 2][col_idx] == checker and \
               board[row_idx + 3][col_idx] == checker:
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row_idx in range(BOARD_HEIGHT - 3):
        for col_idx in range(BOARD_WIDTH - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx + 1][col_idx + 1] == checker and \
               board[row_idx + 2][col_idx + 2] == checker and \
               board[row_idx + 3][col_idx + 3] == checker:
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row_idx in range(3, BOARD_HEIGHT):
        for col_idx in range(BOARD_WIDTH - 3):
            if board[row_idx][col_idx] == checker and \
               board[row_idx - 1][col_idx + 1] == checker and \
               board[row_idx - 2][col_idx + 2] == checker and \
               board[row_idx - 3][col_idx + 3] == checker:
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (i.e., it's a draw)"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    # Create the board
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        # Print the board
        print_board(board)
        
        # Get the current player's checker
        current_checker = CHECKERS[current_player_idx]
        
        # Ask the current player for input
        while True:
            input_str = input(f"Player {current_checker}, please enter a column: ")
            if is_valid_input(input_str, board):
                col_idx = string.ascii_uppercase.index(input_str.upper())
                break
            else:
                print("Invalid input. Please try again.")
        
        # Place the checker
        place_checker(board, col_idx, current_checker)
        
        # Check for a win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            return
        
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            return
        
        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game()
