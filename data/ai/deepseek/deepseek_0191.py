import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Default to first N players

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, etc.)
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print top border
    print('+' + '---+' * COLS)
    
    # Print each row
    for row in board:
        row_str = '|'
        for cell in row:
            row_str += f' {cell} |'
        print(row_str)
        print('+' + '---+' * COLS)

def get_valid_column(current_player):
    """Prompt the player for a valid column input."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A, B, C, etc.).")
            continue
        
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True  # Successfully placed
    
    return False  # Column is full

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check horizontal (left to right)
                if col + 3 < COLS and all(board[row][col + i] == player for i in range(4)):
                    return True
                # Check vertical (up to down)
                if row + 3 < ROWS and all(board[row + i][col] == player for i in range(4)):
                    return True
                # Check diagonal (top-left to bottom-right)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player for i in range(4)):
                    return True
                # Check diagonal (top-right to bottom-left)
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_idx]
    print_board(board)
    
    while True:
        col = get_valid_column(current_player)
        if not place_checker(board, col, current_player):
            print(f"Column {chr(65 + col)} is full. Player {current_player} loses their turn!")
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        current_player = PLAYERS[current_player_idx]

if __name__ == "__main__":
    play_game()
