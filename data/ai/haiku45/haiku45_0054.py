import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """Print the game board in the required format."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")

def get_column_index(column_letter, cols):
    """Convert column letter to index. Returns -1 if invalid."""
    if len(column_letter) != 1:
        return -1
    
    col_index = ord(column_letter.upper()) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index

def is_column_full(board, col):
    """Check if a column is completely filled."""
    if board[0][col] != ' ':
        return True
    return False

def place_checker(board, col, checker):
    """Place a checker in the lowest available row of the given column.
    Returns True if successful, False if column is full."""
    rows = len(board)
    
    # Find the lowest empty row in this column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    return False

def get_valid_column(num_players, current_player, rows, cols):
    """Get a valid column input from the current player."""
    while True:
        user_input = input("Player " + CHECKERS[current_player] + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Convert letter to column index
        col_index = get_column_index(user_input, cols)
        
        # Check if column is valid
        if col_index == -1:
            print("Invalid column. Please enter a letter between A and " + chr(ord('A') + cols - 1) + ".")
            continue
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        # Valid input
        return col_index

def check_win(board, row, col, checker):
    """Check if the last placed checker at (row, col) resulted in a win."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == ' ':
                return False
    
    return True

def get_row_of_checker(board, col):
    """Get the row index where the last checker was placed in a column."""
    rows = len(board)
    
    for row in range(rows):
        if board[row][col] != ' ':
            return row
    
    return -1

def main():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get valid column from current player
        col = get_valid_column(NUM_PLAYERS, current_player, ROWS, COLS)
        
        # Place checker
        checker = CHECKERS[current_player]
        place_checker(board, col, checker)
        
        # Get the row where checker was placed
        row = get_row_of_checker(board, col)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print("Player " + checker + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("Draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
