import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of possible player checkers
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(headers))
    
    for row in board:
        # Print each row with borders
        print('+---' * len(board[0]) + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---' * len(board[0]) + '+')

def get_valid_column(board):
    """Get a valid column input from the current player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(ord('A') + COLS - 1))
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(ord('A') + COLS - 1)}")
            continue
        
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Column is full (shouldn't happen due to validation)

def check_win(board, row, col, player):
    """Check if the current player has won after placing a checker."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (all spaces filled)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

# Main game loop
if __name__ == "__main__":
    board = initialize_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_idx]
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        # Get valid column input
        col = get_valid_column(board)
        
        # Place checker and get row position
        row = place_checker(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            game_over = True
        else:
            # Switch player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            current_player = PLAYERS[current_player_idx]
