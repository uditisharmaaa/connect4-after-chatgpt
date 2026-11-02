import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print each cell in the row
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def is_valid_column(col):
    """Check if the column input is valid (uppercase letter within bounds)."""
    if len(col) != 1:
        return False
    col = col.upper()
    return 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert column letter to its corresponding index (0-based)."""
    return ord(col.upper()) - ord('A')

def is_column_full(board, col_idx):
    """Check if the specified column is full."""
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, player):
    """Place the player's checker in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won with four in a row (horizontal, vertical, diagonal)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Prompt current player for input
        while True:
            col = input(f"Player {current_player}, please enter a column: ").strip()
            if not is_valid_column(col):
                print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
                continue
            
            col_idx = get_column_index(col)
            if is_column_full(board, col_idx):
                print(f"Column {col} is already full. Please choose another column.")
                continue
            
            if place_checker(board, col_idx, current_player):
                break
        
        # Check if current player won
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
