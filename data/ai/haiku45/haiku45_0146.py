import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return a board with all empty spaces."""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print horizontal border
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()

def is_valid_input(user_input, board):
    """
    Check if the user input is valid.
    Valid input is a single uppercase letter corresponding to a non-full column.
    """
    if len(user_input) != 1:
        return False
    
    if not user_input.isupper() or not user_input.isalpha():
        return False
    
    col_index = ord(user_input) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def get_player_move(player_checker, board):
    """Get and validate the player's move."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if is_valid_input(user_input, board):
            return ord(user_input) - ord('A')
        
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full (should not happen with validation)

def check_win(board, row, col, checker):
    """
    Check if the last placed checker at (row, col) results in a win.
    Returns True if there are 4 checkers in a row, False otherwise.
    """
    # Check horizontal
    count = 1
    
    # Count to the left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Count to the right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    
    # Count upward
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    # Count downward
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Count up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    # Count down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Count up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Count down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        
        # Get player's move
        col = get_player_move(current_checker, board)
        
        # Place checker and get the row where it was placed
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    play_game()

if __name__ == "__main__":
    main()
