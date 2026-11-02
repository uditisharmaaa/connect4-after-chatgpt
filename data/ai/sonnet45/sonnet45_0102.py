import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")

def is_valid_column(column_letter, board):
    """Check if the column letter is valid and not full."""
    # Check if it's a single uppercase letter
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(column_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full (top row should be empty)
    if board[0][col_index] != ' ':
        return False
    
    return True

def place_checker(board, column_letter, checker):
    """Place the checker in the specified column."""
    col_index = ord(column_letter) - 65
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    
    return -1, -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    # Check diagonal
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    # Check diagonal
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    """Main game function."""
    # Create board
    board = create_board()
    
    # Set up players
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        current_checker = players[current_player_index]
        
        # Get player input
        valid_input = False
        while not valid_input:
            column_input = input("Player " + current_checker + ", please enter a column: ")
            
            if is_valid_column(column_input, board):
                valid_input = True
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        row, col = place_checker(board, column_input, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    main()
