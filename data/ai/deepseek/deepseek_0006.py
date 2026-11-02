import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only use needed players

def initialize_board():
    """Create an empty board with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column headers
    header = '   ' + '   '.join(chr(ord('A') + i) for i in range(BOARD_COLS))
    print(header)
    
    # Print each row with borders
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    
    # Print bottom border
    print('+---' * BOARD_COLS + '+')

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_char = col.upper()
    return 'A' <= col_char <= chr(ord('A') + BOARD_COLS - 1)

def get_column_index(col):
    """Convert column letter to 0-based index."""
    return ord(col.upper()) - ord('A')

def drop_checker(board, col, checker):
    """Place the checker in the lowest empty row of the column."""
    col_index = get_column_index(col)
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the player with the given checker has won."""
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

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checker = PLAYERS[current_player]
    
    while True:
        os.system('clear')
        print_board(board)
        
        print(f"Player {checker}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid column. Please enter a letter from A to " + chr(ord('A') + BOARD_COLS - 1))
            input("Press Enter to continue...")
            continue
        
        col_char = col_input[0]
        col_index = get_column_index(col_char)
        
        if not drop_checker(board, col_char, checker):
            print("That column is full. You lose your turn.")
            input("Press Enter to continue...")
        
        if check_win(board, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS
        checker = PLAYERS[current_player]

if __name__ == "__main__":
    main()
