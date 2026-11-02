import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Possible player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [ [' ' for _ in range(COLS)] for _ in range(ROWS) ]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def get_player_turn(players, current_player_index):
    """Get the current player's input for their turn."""
    while True:
        try:
            col = input(f"Player {players[current_player_index]}, please enter a column: ").upper()
            if len(col) != 1 or col < 'A' or col > chr(ord('A') + COLS - 1):
                print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
                continue
            return ord(col) - ord('A')  # Convert letter to column index (0-based)
        except Exception as e:
            print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible.
    Returns the row index where the checker was placed, or -1 if the column is full."""
    for row in range(ROWS-1, -1, -1):  # Start from the bottom row
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full

def check_win(board, row, col, checker):
    """Check if the current move results in a win.
    Returns True if there are 4 consecutive checkers in any direction."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # The current checker is already placed
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (a draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize board and players
    board = initialize_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print_board(board)
    
    while True:
        # Get current player's move
        col = get_player_turn(players, current_player_index)
        
        # Place the checker
        row = place_checker(board, col, players[current_player_index])
        if row == -1:
            print("Column is full. You lose your turn.")
        else:
            print_board(board)
            
            # Check for win
            if check_win(board, row, col, players[current_player_index]):
                print(f"Player {players[current_player_index]} won!")
                break
            
            # Check for draw
            if is_draw(board):
                print("Game ended in a draw!")
                break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
