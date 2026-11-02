import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with spaces"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column not full)"""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win"""
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

def check_draw(board):
    """Check if the board is full (draw)"""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_column_input():
    """Get and validate column input from user"""
    while True:
        user_input = input()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter: ", end="")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper() or not user_input.isalpha():
            print("Invalid input. Please enter an uppercase letter: ", end="")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is within board range
        if col < 0 or col >= COLS:
            print("Invalid input. Column out of range. Please enter a valid column: ", end="")
            continue
        
        return col

def play_game():
    """Main game loop"""
    board = create_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        col = get_column_input()
        
        # Check if move is valid
        if not is_valid_move(board, col):
            print_board(board)
            print(f"Column is full. Player {checker} loses this turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        row = place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
