import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print('+' + '---+' * COLS)
    
    for row in board:
        # Print row content
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        # Print row border
        print('+' + '---+' * COLS)

def get_valid_column(player, board):
    """Get a valid column choice from the player."""
    while True:
        try:
            col = input(f"Player {player}, please enter a column: ").upper()
            if not col or ord(col) < 65 or ord(col) >= 65 + COLS:
                print(f"Invalid column. Please choose a letter from A to {chr(65 + COLS - 1)}.")
                continue
            
            col_idx = ord(col) - 65
            
            # Check if column is full
            if board[0][col_idx] != ' ':
                print("Column is full. Please choose another column.")
                continue
                
            return col_idx
        except Exception:
            print(f"Invalid input. Please choose a letter from A to {chr(65 + COLS - 1)}.")

def place_checker(board, col_idx, checker):
    """Place a checker in the specified column at the lowest available row."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return (row_idx, col_idx)
    return None

def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    # Directions: (dr, dc) where dr is delta-row and dc is delta-col
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Includes the current checker
        
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]
    winner = None
    
    while True:
        os.system('clear')
        print_board(board)
        
        if winner is not None:
            print(f"Player {winner} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
            
        checker = checkers[current_player]
        col_idx = get_valid_column(checker, board)
        row, col = place_checker(board, col_idx, checker)
        
        if check_win(board, row, col, checker):
            winner = checker
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
