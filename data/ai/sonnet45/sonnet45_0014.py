import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the specified dimensions."""
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for col in range(COLS):
            print(board[row][col] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
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
    start_row = row - min(row, col)
    start_col = col - min(row, col)
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
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
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
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move():
    """Get and validate player input."""
    while True:
        move = input()
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter: ", end="")
            continue
        
        # Check if input is an uppercase letter
        if not move.isupper() or not move.isalpha():
            print("Invalid input. Please enter an uppercase letter: ", end="")
            continue
        
        # Convert letter to column index
        col = ord(move) - 65
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print("Invalid column. Please enter a valid column letter: ", end="")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        col = get_player_move()
        
        # Check if the column is full
        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place the checker
        row = place_checker(board, col, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for a draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
