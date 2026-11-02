import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board(rows, cols):
    """Create and initialize the game board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def is_valid_column(col, cols):
    """Check if the column input is valid."""
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - ord('A')
    return 0 <= col_index < cols

def place_checker(board, col, checker):
    """Place the checker in the specified column."""
    col_index = ord(col.upper()) - ord('A')
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the current player has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - 3):
        for col in range(3, cols):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col = input().strip().upper()
        
        if not is_valid_column(col, COLS):
            print("Invalid column! Please try again.")
            continue
        
        if not place_checker(board, col, current_player):
            print("Column is full! Please try another column.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
