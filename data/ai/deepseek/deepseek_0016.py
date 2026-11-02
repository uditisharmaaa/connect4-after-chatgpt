import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(len(board[0]))]) + '  '
    print(header)
    
    # Print the board rows with borders
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def is_valid_column(col, max_col):
    """Check if the input column is valid (within bounds and single uppercase letter)."""
    if len(col) != 1:
        return False
    char = col.upper()
    return 'A' <= char <= chr(ord('A') + max_col - 1)

def get_player_move(player, max_col):
    """Get and validate player's column choice."""
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if is_valid_column(col, max_col):
            return ord(col) - ord('A')  # Convert to 0-based index
        print("Invalid column. Please try again.")

def drop_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # Column is full

def check_winner(board, player):
    """Check if the player has four in a row horizontally, vertically, or diagonally."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to run the Connect 4 game."""
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    players_list = PLAYERS[:NUM_PLAYERS]
    
    while True:
        print_board(board)
        player = players_list[current_player_idx]
        col = get_player_move(player, COLS)
        
        if drop_checker(board, col, player):
            if check_winner(board, player):
                print_board(board)
                print(f"Player {player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print("Column is full. You lose your turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
