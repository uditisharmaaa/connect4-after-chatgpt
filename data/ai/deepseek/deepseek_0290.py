import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Create and return an empty game board with given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the screen
    
    # Print column headers (A, B, C...)
    print(' ' + '   '.join([chr(65 + i) for i in range(len(board[0]))]))
    
    # Print the board with borders
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print(border)

def get_valid_move(board, player):
    """
    Prompt the player for a move and validate it.
    Returns the column index if valid, None if column is full.
    """
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            if len(col_input) != 1 or not col_input.isalpha():
                print("Invalid input. Please enter a single letter from A to", chr(65 + len(board[0]) - 1))
                continue
                
            col = ord(col_input) - ord('A')
            if col < 0 or col >= len(board[0]):
                print("Column out of range. Please try again.")
                continue
                
            # Check if column is full
            if board[0][col] != ' ':
                print("Column is full. You lose this turn.")
                return None
                
            return col
        except EOFError:
            print("Invalid input. Please try again.")
            continue

def place_checker(board, col, player):
    """
    Place the player's checker in the specified column.
    Returns the row where the checker was placed.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return None  # This shouldn't happen since we checked earlier

def check_win(board, row, col, player):
    """
    Check if the last move resulted in a win.
    Returns True if player has won, False otherwise.
    """
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Include the current piece
        
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
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    print("Welcome to Connect 4!")
    print(f"Player {current_player} goes first.")
    print()
    
    while True:
        print_board(board)
        
        col = get_valid_move(board, current_player)
        if col is None:  # Column was full, skip turn
            current_player = players[(players.index(current_player) + 1) % len(players)]
            continue
            
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
            
        if check_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
            
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    play_game()
