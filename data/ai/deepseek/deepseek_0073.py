import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First NUM_PLAYERS checkers

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print board rows
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print(border)

def is_valid_column(col):
    """Check if column input is valid (uppercase letter within bounds)."""
    if len(col) != 1:
        return False
    col_idx = ord(col) - ord('A')
    return 0 <= col_idx < BOARD_COLS

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    col_idx = ord(col) - ord('A')
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal, vertical, and both diagonals
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    if check_line(board, row, col, dr, dc, player):
                        return True
    return False

def check_line(board, row, col, dr, dc, player):
    """Check if there are 4 consecutive player checkers starting at (row,col) in direction (dr,dc)."""
    for i in range(1, 4):
        r, c = row + i * dr, col + i * dc
        if r < 0 or r >= BOARD_ROWS or c < 0 or c >= BOARD_COLS:
            return False
        if board[r][c] != player:
            return False
    return True

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col = input().strip().upper()
        
        # Validate input
        if not is_valid_column(col):
            print("Invalid input! Please enter a valid column letter (A-G).")
            continue
        
        # Attempt to place checker
        if place_checker(board, col, current_player):
            # Check for win
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
            
            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    play_game()
