import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for row in board:
        print("+" + "---+" * NUM_COLS)
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+" + "---+" * NUM_COLS)

def is_valid_input(column_input, board):
    """Check if the input is valid."""
    # Check if input is a single character
    if len(column_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not column_input.isupper() or not column_input.isalpha():
        return False
    
    # Check if column is within board range
    col_index = ord(column_input) - ord('A')
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column_input, checker):
    """Place a checker in the specified column."""
    col_index = ord(column_input) - ord('A')
    
    # Find the lowest available row
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index, col_index
    
    return -1, -1

def check_win(board, row, col, checker):
    """Check if the current player has won."""
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row + min(NUM_ROWS - 1 - row, col)
    start_col = col - min(NUM_ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < NUM_COLS:
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
    """Check if the board is full (draw)."""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            if is_valid_input(column_input, board):
                break
            else:
                print("Invalid input. Please try again.")
        
        # Place the checker
        row, col = place_checker(board, column_input, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
