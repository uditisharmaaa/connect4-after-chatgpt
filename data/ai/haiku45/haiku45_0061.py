import os
import random

# Configuration constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print('  ', end='')
    for col in range(BOARD_WIDTH):
        print(f'{chr(65 + col):^3}', end=' ')
    print()
    
    # Print board with borders
    for row in range(BOARD_HEIGHT):
        print('+---' * BOARD_WIDTH + '+')
        print('|', end='')
        for col in range(BOARD_WIDTH):
            print(f' {board[row][col]} |', end='')
        print()
    print('+---' * BOARD_WIDTH + '+')

def is_valid_column(column_input):
    """Check if the input is a valid column."""
    if len(column_input) != 1:
        return False
    col_idx = ord(column_input.upper()) - ord('A')
    return 0 <= col_idx < BOARD_WIDTH

def get_valid_column():
    """Get and validate column input from player."""
    while True:
        column_input = input("Enter column (A-" + chr(64 + BOARD_WIDTH) + "): ").strip()
        if is_valid_column(column_input):
            return ord(column_input.upper()) - ord('A')
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful."""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - WIN_LENGTH + 1):
        for col in range(BOARD_WIDTH - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_HEIGHT - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_WIDTH):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(BOARD_WIDTH))

def play_game():
    """Main game loop."""
    board = initialize_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        
        col = get_valid_column()
        
        if not place_checker(board, col, current_checker):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    play_game()
