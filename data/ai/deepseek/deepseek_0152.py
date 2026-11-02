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
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + ('---+' * COLS))
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col.isalpha() and ord(col) - ord('A') >= 0 and ord(col) - ord('A') < COLS

def get_column_index(col):
    """Convert column letter to index."""
    return ord(col.upper()) - ord('A')

def drop_piece(board, col, piece):
    """Drop a piece into the specified column."""
    col_index = get_column_index(col)
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = piece
            return True
    return False

def check_win(board, piece):
    """Check if the specified piece has a winning line."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == piece for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ")
        col = input().strip()
        
        if not is_valid_column(col):
            print("Invalid input. Please enter a letter from A to G.")
            continue
        
        if not drop_piece(board, col, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
