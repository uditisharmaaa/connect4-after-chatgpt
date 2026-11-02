import os
import random

# Constants for the board
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'] # Max 5 players
NUM_PLAYERS = 2  # Change this as needed (between 2 and 5)

def create_board(rows, columns):
    """Create a game board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    labels = '  ' + '   '.join(chr(i) for i in range(ord('A'), ord('A') + COLUMNS))
    print(labels)
    
    # Print the board
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def is_valid_column(column):
    """Check if entered column is within the valid range."""
    return 'A' <= column < chr(ord('A') + COLUMNS)

def is_column_full(board, column):
    """Check if a column is full."""
    col_idx = ord(column) - ord('A')
    return board[0][col_idx] != ' '

def drop_checker(board, column, checker):
    """Drop a checker into the board at the specified column."""
    col_idx = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return True
    return False  # This case should never occur due to prior checks

def check_for_win(board, checker):
    """Check the board for a win condition for the given checker."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Check for a draw condition."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        player_symbol = PLAYERS[current_player]
        print(f"Player {player_symbol}, please enter a column:")
        
        column = input().strip().upper()
        
        while not is_valid_column(column) or is_column_full(board, column):
            print("Invalid input or full column. Please try again.")
            column = input().strip().upper()
        
        drop_checker(board, column, player_symbol)
        
        if check_for_win(board, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break
        
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Change to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
