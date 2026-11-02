import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    os.system('clear')
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)])
    print(header)
    # Print top border
    print('+' + ('---+' * BOARD_COLS))
    # Print each row
    for row in board:
        # Print row content
        row_str = '|'
        for cell in row:
            row_str += f' {cell} |'
        print(row_str)
        # Print bottom border
        print('+' + ('---+' * BOARD_COLS))

def is_valid_column(col):
    """Check if the column is valid (within bounds and not full)."""
    if not col.isalpha() or len(col) != 1:
        return False
    col_index = ord(col.upper()) - ord('A')
    return 0 <= col_index < BOARD_COLS

def drop_checker(board, col, player):
    """Drop a checker into the specified column."""
    col_index = ord(col.upper()) - ord('A')
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the player has won (4 in a row horizontally, vertically, or diagonally)."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and
                board[row][col+1] == player and
                board[row][col+2] == player and
                board[row][col+3] == player):
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == player and
                board[row+1][col] == player and
                board[row+2][col] == player and
                board[row+3][col] == player):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and
                board[row-1][col+1] == player and
                board[row-2][col+2] == player and
                board[row-3][col+3] == player):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and
                board[row+1][col+1] == player and
                board[row+2][col+2] == player and
                board[row+3][col+3] == player):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        # Get player input
        while True:
            col = input(f"Player {current_player}, please enter a column: ")
            if is_valid_column(col) and drop_checker(board, col, current_player):
                break
            print("Invalid input. Please try again.")
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
