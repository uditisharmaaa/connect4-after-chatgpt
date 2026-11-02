import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create a new empty board with the specified dimensions."""
    board = []
    for _ in range(ROWS):
        row = [' ' for _ in range(COLS)]
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print top border
    border = '+' + ('---+' * COLS)
    print(border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(border)

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if not col.isalpha() or len(col) != 1:
        return False
    
    col_idx = ord(col.upper()) - ord('A')
    if col_idx < 0 or col_idx >= COLS:
        return False
    
    # Check if the column has space
    return board[0][col_idx] == ' '

def place_checker(col, player, board):
    """Place the player's checker in the specified column."""
    col_idx = ord(col.upper()) - ord('A')
    
    # Find the first empty row from the bottom
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return True
    
    return False

def check_winner(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == player and
                board[r][c+1] == player and
                board[r][c+2] == player and
                board[r][c+3] == player):
                return True
    
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == player and
                board[r+1][c] == player and
                board[r+2][c] == player and
                board[r+3][c] == player):
                return True
    
    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == player and
                board[r+1][c+1] == player and
                board[r+2][c+2] == player and
                board[r+3][c+3] == player):
                return True
    
    # Check diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == player and
                board[r-1][c+1] == player and
                board[r-2][c+2] == player and
                board[r-3][c+3] == player):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ", end='')
        
        col = input().strip().upper()
        
        if not is_valid_column(col, board):
            print("Invalid column. Please try again.")
            continue
        
        place_checker(col, current_player, board)
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
