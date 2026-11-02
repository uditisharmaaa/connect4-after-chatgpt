import os
import random

# Configuration constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in a formatted manner."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()

def get_column_input(current_player, cols):
    """Get and validate column input from the current player."""
    while True:
        try:
            user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            
            # Validate input
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col_index = ord(user_input) - ord('A')
            
            if col_index < 0 or col_index >= cols:
                print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
                continue
            
            return col_index
        except ValueError:
            print("Invalid input. Please try again.")

def place_checker(board, col, player_checker):
    """
    Place a checker in the given column.
    Returns True if successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    return False

def check_win(board, last_row, last_col, player_checker):
    """Check if the current player has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    col = last_col - 1
    while col >= 0 and board[last_row][col] == player_checker:
        count += 1
        col -= 1
    # Check right
    col = last_col + 1
    while col < cols and board[last_row][col] == player_checker:
        count += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check down
    row = last_row + 1
    while row < rows and board[row][last_col] == player_checker:
        count += 1
        row += 1
    # Check up
    row = last_row - 1
    while row >= 0 and board[row][last_col] == player_checker:
        count += 1
        row -= 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    row, col = last_row - 1, last_col - 1
    while row >= 0 and col >= 0 and board[row][col] == player_checker:
        count += 1
        row -= 1
        col -= 1
    # Check down-right
    row, col = last_row + 1, last_col + 1
    while row < rows and col < cols and board[row][col] == player_checker:
        count += 1
        row += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    row, col = last_row - 1, last_col + 1
    while row >= 0 and col < cols and board[row][col] == player_checker:
        count += 1
        row -= 1
        col += 1
    # Check down-left
    row, col = last_row + 1, last_col - 1
    while row < rows and col >= 0 and board[row][col] == player_checker:
        count += 1
        row += 1
        col -= 1
    if count >= WIN_LENGTH:
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
    # Initialize board
    board = create_board(ROWS, COLS)
    
    # Print initial board
    print_board(board)
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]
    
    # Game loop
    while True:
        # Get input from current player
        col = get_column_input(current_player_checker, COLS)
        
        # Find the row where the checker will be placed
        last_row = -1
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == " ":
                last_row = row
                break
        
        # Check if column is full
        if last_row == -1:
            print("Column is full. You lose your turn.")
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = PLAYER_CHECKERS[current_player_index]
            continue
        
        # Place the checker
        place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, last_row, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player_checker = PLAYER_CHECKERS[current_player_index]

def main():
    """Entry point of the program."""
    play_game()

if __name__ == "__main__":
    main()
