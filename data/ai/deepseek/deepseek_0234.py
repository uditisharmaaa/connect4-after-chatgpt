import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of player tokens in order
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear screen before printing
    os.system('clear')
    
    # Print column headers (letters A-G)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print each cell in the row
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row separator
        print('+' + ('---+' * COLS))

def get_valid_column(board):
    """
    Prompt the current player for a column and validate the input.
    Keep asking until a valid column is provided.
    """
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        
        # Check if input is a single alphabetic character
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter from A to " + chr(64 + COLS))
            continue
        
        # Convert to column index (0-based)
        col = ord(col_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(64 + COLS)}")
            continue
        
        # Check if column is full
        if board[0][col] != ' ':
            print("That column is full. Please choose another.")
            continue
            
        return col

def place_checker(board, col, player_token):
    """
    Place the player's token in the lowest empty row of the specified column.
    Returns the row where the token was placed.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return row
    return -1  # Column is full (shouldn't happen if input validated)

def check_win(board, row, col, player_token):
    """
    Check if the last move resulted in a win (4 in a row in any direction).
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # include the current piece
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
            
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
            
        if count >= 4:
            return True
            
    return False

def is_board_full(board):
    """Check if the board is completely full (draw)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    global current_player  # track whose turn it is
    
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)  # randomly choose first player
    
    while True:
        player_token = PLAYER_TOKENS[current_player]
        print_board(board)
        
        col = get_valid_column(board)
        row = place_checker(board, col, player_token)
        
        # Check for win
        if check_win(board, row, col, player_token):
            print_board(board)
            print(f"Player {player_token} won!")
            break
            
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("Game ended in a draw!")
            break
            
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
