import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create an empty game board with the given dimensions."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, etc.)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLUMNS)]))
    
    # Print the board rows with separators
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def get_random_first_player():
    """Return a random player index to start the game."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(column_input):
    """Check if the user's column input is valid."""
    if not column_input or len(column_input) != 1:
        return False
    
    col_char = column_input.upper()
    return 'A' <= col_char <= chr(65 + COLUMNS - 1)

def get_column_index(column_input):
    """Convert the column letter to a 0-based index."""
    return ord(column_input.upper()) - ord('A')

def place_checker(board, column, player_symbol):
    """Place the player's checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            return row
    return -1

def check_win(board, row, col, player_symbol):
    """Check if the last move resulted in a win (4 in a row)."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current cell is already the player's
        
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (a draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = get_random_first_player()
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    print(f"Player {player_symbols[current_player]} starts first!")
    
    while True:
        print_board(board)
        
        # Get valid column input
        column_input = input(f"Player {player_symbols[current_player]}, please enter a column: ").strip()
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a letter from A to " + chr(65 + COLUMNS - 1))
            continue
        
        column = get_column_index(column_input)
        
        # Place checker
        row = place_checker(board, column, player_symbols[current_player])
        if row == -1:
            print("Column is full. Try another column.")
            continue
        
        # Check for win
        if check_win(board, row, column, player_symbols[current_player]):
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
