import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---' * NUM_COLS + '+')

def get_valid_column(current_player):
    """Get a valid column input from the current player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or ord(col_input) < 65 or ord(col_input) >= 65 + NUM_COLS:
            print(f"Invalid input. Please enter a letter from A to {chr(65 + NUM_COLS - 1)}.")
            continue
        
        col = ord(col_input) - 65  # Convert to 0-based index
        return col

def drop_checker(board, col, checker):
    """Drop the checker into the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column is full

def check_win(board, row, col, checker):
    """Check if the current move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check for win
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_idx]
    game_over = False
    
    print_board(board)
    
    while not game_over:
        col = get_valid_column(current_player)
        if drop_checker(board, col, current_player):
            print_board(board)
            row = next((r for r in range(NUM_ROWS) if board[r][col] == current_player), -1)
            if check_win(board, row, col, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif is_draw(board):
                print("It's a draw!")
                game_over = True
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            current_player = PLAYERS[current_player_idx]
        else:
            print(f"Column {chr(65 + col)} is full. Player {current_player} loses their turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            current_player = PLAYERS[current_player_idx]

if __name__ == "__main__":
    main()
