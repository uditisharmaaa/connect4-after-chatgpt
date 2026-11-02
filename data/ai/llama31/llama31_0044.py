import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the board with column labels"""
    print('  A', 'B', 'C', 'D', 'E', 'F', 'G', sep='   ')
    print('+---+' + '+---' * (NUM_COLS - 1))
    for row in board:
        print('|', end='   ')
        for cell in row:
            print(cell, end='   |')
        print()
        print('+---+' + '+---' * (NUM_COLS - 1))

def get_player_checker(player_id):
    """Get the checker for the given player ID"""
    return CHECKERS[player_id]

def is_valid_input(input_str):
    """Check if the input is a valid column label"""
    return input_str.upper() in 'ABCDEFG'

def get_column_index(input_str):
    """Get the column index from the input string"""
    return ord(input_str.upper()) - ord('A')

def is_valid_move(board, col):
    """Check if the move is valid (column is not full)"""
    return board[0][col] == ' '

def make_move(board, player_id, col):
    """Make a move by placing the checker in the given column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = get_player_checker(player_id)
            return

def check_win(board, player_id):
    """Check if the player has won"""
    checker = get_player_checker(player_id)
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    # Create the board
    board = create_board()

    # Randomly select the first player
    current_player_id = random.randint(0, NUM_PLAYERS - 1)

    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Get the player's input
        input_str = input(f"Player {get_player_checker(current_player_id)}, please enter a column: ")

        # Validate the input
        if not is_valid_input(input_str):
            print("Invalid input. Please enter a column label (A-G).")
            continue

        # Get the column index
        col = get_column_index(input_str)

        # Check if the move is valid
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue

        # Make the move
        make_move(board, current_player_id, col)

        # Check for a win
        if check_win(board, current_player_id):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(current_player_id)} won!")
            break

        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_id = (current_player_id + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
