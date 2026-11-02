import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Initialize the Connect 4 board with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Clear the screen and print the board."""
    os.system('clear')
    column_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLUMNS]
    print('  ' + '   '.join(column_labels))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_column(column_choice):
    """Check if the input column is valid."""
    return column_choice in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLUMNS]

def is_column_full(board, col_idx):
    """Check if a column is full."""
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, checker):
    """Place the checker in the chosen column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return

def check_win(board, checker):
    """Check for a win condition for the given checker."""
    # Check horizontal, vertical and diagonal directions
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
            
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is completely filled."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_four():
    """Main function to run the Connect Four game."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}, please enter a column:")

        column_choice = input().strip().upper()
        
        if not is_valid_column(column_choice):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_idx = ord(column_choice) - ord('A')
        
        if is_column_full(board, col_idx):
            print(f"Column {column_choice} is full. Choose another column.")
            continue
        
        place_checker(board, col_idx, player_checkers[current_player])

        if check_win(board, player_checkers[current_player]):
            print_board(board)
            print(f"Player {player_checkers[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_four()
