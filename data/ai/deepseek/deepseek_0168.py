import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2  # Can be between 2 and 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

def initialize_board():
    """Create a new empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)])
    print(header)
    
    # Print the board rows with separators
    separator = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(separator)
        line = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(line)
    print(separator)

def is_valid_column(col):
    """Check if the input column is valid (uppercase letter within range)."""
    if len(col) != 1:
        return False
    char = col.upper()
    return 'A' <= char <= chr(65 + BOARD_COLS - 1)

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible.
    Returns True if placement was successful, False otherwise."""
    col_index = ord(col.upper()) - ord('A')
    column_full = True
    
    # Find the lowest empty row in the column
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            column_full = False
            break
    
    return not column_full

def check_winner(board, checker):
    """Check if the specified checker has won (4 in a row horizontally, vertically, or diagonally)."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    players_list = PLAYERS[:NUM_PLAYERS]
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        print(f"Player {players_list[current_player]}, please enter a column:", end=' ')
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid column! Please enter a valid column (A-G).")
            input("Press Enter to try again...")
            continue
        
        if not place_checker(board, col_input, players_list[current_player]):
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_winner(board, players_list[current_player]):
                clear_screen()
                print_board(board)
                print(f"Player {players_list[current_player]} won!")
                game_over = True
                break
            
            if is_board_full(board):
                clear_screen()
                print_board(board)
                print("Game over! It's a draw.")
                game_over = True
                break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
