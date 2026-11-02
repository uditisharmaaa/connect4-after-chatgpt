import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and grid lines."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print separator line
    print("  " + "+---" * COLS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
        print("  " + "+---" * COLS + "+")


def get_column_input(player_checker):
    """Get and return valid column input from player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is within board range
        if col < 0 or col >= COLS:
            print("Invalid input. Column is out of range.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place checker in the specified column at the lowest available position.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    # Start from the bottom row and move up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    # Column is full
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last move at (row, col) resulted in a win.
    Returns True if player wins, False otherwise.
    """
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
    # Find starting position
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    # Count along diagonal
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
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
    
    # Count along diagonal
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def main():
    """Main game loop."""
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        current_checker = CHECKERS[current_player_index]
        
        # Get column input from player
        col = get_column_input(current_checker)
        
        # Place checker
        row = place_checker(board, col, current_checker)
        
        # Check if column was full
        if row == -1:
            print_board(board)
            print("Column is full. You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
