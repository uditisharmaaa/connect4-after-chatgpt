import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Create and return an empty board with all spaces initialized to whitespace."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        letter = chr(ord('A') + i)
        print(f" {letter}  ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for i in range(rows):
        print("|", end="")
        for j in range(cols):
            print(f" {board[i][j]} |", end="")
        print()
        print("+---" * cols + "+")

def get_valid_column(board):
    """Get a valid column input from the player."""
    cols = len(board[0])
    
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("That column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1

def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win at the given position."""
    cols = len(board[0])
    count = 0
    
    # Count checkers to the left
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count checkers to the right
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win at the given position."""
    rows = len(board)
    count = 0
    
    # Count checkers above
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count checkers below
    for r in range(row + 1, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_diagonal_win(board, row, col, checker):
    """Check if there is a diagonal win at the given position (both directions)."""
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal going down-right to up-left
    count = 0
    
    # Count up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal going down-left to up-right
    count = 0
    
    # Count up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win(board, row, col, checker):
        return True
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Choose a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Print current player
        print(f"Player {checker}, please enter a column:")
        
        # Get valid column input
        col = get_valid_column(board)
        
        # Place checker
        row = place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
