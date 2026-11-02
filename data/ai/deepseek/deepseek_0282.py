import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for players in order: X, O, V, H, M
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---+' * NUM_COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * NUM_COLS)

def get_random_first_player():
    """Randomly select the first player."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(col_input):
    """Check if the column input is valid."""
    if len(col_input) != 1:
        return False
    col = col_input.upper()
    return col.isalpha() and ord(col) - 65 < NUM_COLS

def get_column_index(col_input):
    """Convert column letter to index."""
    return ord(col_input.upper()) - 65

def place_checker(board, col, checker):
    """Place the checker in the lowest available row in the column.
    Returns the row where the checker was placed, or -1 if column is full."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontally
    count = 1
    # Left
    for c in range(col - 1, max(-1, col - 4), -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Right
    for c in range(col + 1, min(NUM_COLS, col + 4)):
        if board[row][c] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check vertically
    count = 1
    # Up
    for r in range(row - 1, max(-1, row - 4), -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    # Down
    for r in range(row + 1, min(NUM_ROWS, row + 4)):
        if board[r][col] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    # Top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and count < 4:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    # Bottom-right
    r, c = row + 1, col + 1
    while r < NUM_ROWS and c < NUM_COLS and count < 4:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    # Top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < NUM_COLS and count < 4:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    # Bottom-left
    r, c = row + 1, col - 1
    while r < NUM_ROWS and c >= 0 and count < 4:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    if count >= 4:
        return True

    return False

def is_draw(board):
    """Check if the game is a draw (all cells are filled)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player()
    player_checker = PLAYER_CHECKERS[current_player]

    print("Welcome to Connect 4!")
    print(f"Player {player_checker} goes first.")
    print_board(board)

    while True:
        # Get player input
        col_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Validate input
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a letter from A to", chr(65 + NUM_COLS - 1))
            continue
        
        col = get_column_index(col_input)
        
        # Place checker
        row = place_checker(board, col, player_checker)
        if row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        # Print board after placement
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS
        player_checker = PLAYER_CHECKERS[current_player]

if __name__ == "__main__":
    main()
