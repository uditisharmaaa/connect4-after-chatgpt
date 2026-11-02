import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the specified dimensions."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in board:
        print("+---" * COLS + "+")
        print("| ", end="")
        for cell in row:
            print(cell + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(board, col):
    """Check if a column is valid and has space."""
    if col < 0 or col >= COLS:
        return False
    # Check if top row has space
    if board[0][col] != " ":
        return False
    return True

def drop_checker(board, col, checker):
    """Drop a checker into the specified column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ")
            
            # Check if input is a single character
            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter.")
                continue
            
            # Check if input is a letter
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            # Convert to uppercase and get column index
            user_input = user_input.upper()
            col = ord(user_input) - 65
            
            # Check if column is valid
            if col < 0 or col >= COLS:
                print("Invalid column. Please choose a column between A and " + chr(65 + COLS - 1) + ".")
                continue
            
            # Check if column has space
            if not is_valid_column(board, col):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Drop the checker
        row = drop_checker(board, col, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
