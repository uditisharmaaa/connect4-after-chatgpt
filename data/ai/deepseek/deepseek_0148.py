import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with dimensions ROWS x COLS."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board):
    """Print the current state of the game board."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print board rows with separators
    print('+' + ('---+' * COLS))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def is_valid_column(col, board):
    """Check if the column is valid and not full."""
    if not col or len(col) != 1:
        return False
    col_char = col.upper()
    if not col_char.isalpha():
        return False
    col_idx = ord(col_char) - ord('A')
    if col_idx < 0 or col_idx >= COLS:
        return False
    return board[0][col_idx] == ' '

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    col_idx = ord(col.upper()) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the player with the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (all positions filled with no winner)."""
    return all(cell != ' ' for row in board for cell in row)

def get_player_move(player, board):
    """Get a valid column from the player."""
    while True:
        col = input(f"Player {player}, please enter a column: ").strip()
        if is_valid_column(col, board):
            return col.upper()
        print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + COLS - 1)))

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYER_CHECKERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        if is_draw(board):
            print("Draw! The board is full.")
            break
        
        col = get_player_move(current_player, board)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Switch to next player
        current_player = PLAYER_CHECKERS[(PLAYER_CHECKERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
