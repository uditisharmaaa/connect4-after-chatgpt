import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of possible player checkers
PLAYER_CHECKS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = [chr(ord('A') + i) for i in range(COLS)]
    print('  ' + '   '.join(header))
    
    # Print the board rows with borders
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+' + '---+' * COLS)

def get_random_start_player(num_players):
    """Randomly select the starting player."""
    return random.randint(0, num_players - 1)

def is_valid_column(column):
    """Validate if the entered column is within bounds."""
    return len(column) == 1 and 'A' <= column <= chr(ord('A') + COLS - 1)

def place_checker(board, column, checker):
    """
    Place the checker in the lowest available row in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    col_idx = ord(column) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has 4 in a row (horizontally, vertically, or diagonally)."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonally (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(cell != ' ' for row in board for cell in row)

def switch_player(current_player, num_players):
    """Switch to the next player."""
    return (current_player + 1) % num_players

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = PLAYER_CHECKS[:NUM_PLAYERS]
    current_player = get_random_start_player(NUM_PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        checker = players[current_player]
        print(f"Player {checker}, please enter a column:")
        
        while True:
            column = input().strip().upper()
            if not is_valid_column(column):
                print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + COLS - 1)}:")
            elif not place_checker(board, column, checker):
                print("Column is full. Please choose another column:")
            else:
                break
        
        if check_win(board, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = switch_player(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
