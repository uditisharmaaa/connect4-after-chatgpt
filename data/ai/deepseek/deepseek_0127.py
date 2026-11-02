import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---+' * COLS)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col_idx = ord(column.upper()) - ord('A')
    return 0 <= col_idx < COLS

def place_checker(board, col_idx, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won by getting 4 in a row."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row][col+1] == checker and
                board[row][col+2] == checker and
                board[row][col+3] == checker):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and
                board[row+1][col] == checker and
                board[row+2][col] == checker and
                board[row+3][col] == checker):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == checker and
                board[row+1][col-1] == checker and
                board[row+2][col-2] == checker and
                board[row+3][col-3] == checker):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        print(f"Player {current_player}, please enter a column: ")
        column = input().strip().upper()
        
        # Validate input
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter (A-G).")
            input("Press Enter to continue...")
            continue
        
        col_idx = ord(column) - ord('A')
        
        # Try to place the checker
        if not place_checker(board, col_idx, current_player):
            print("Column is full. Try another column.")
            input("Press Enter to continue...")
            continue
        
        # Check for win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
