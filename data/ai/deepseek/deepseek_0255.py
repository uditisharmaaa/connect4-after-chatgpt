import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with columns labeled A, B, C, etc."""
    # Clear the screen
    os.system('clear')  # Use 'cls' if on Windows
    
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)])
    print(header)
    
    # Print each row
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---' * COLS + '+')

def get_player_move(player, board):
    """Get a valid column from the player."""
    valid_columns = [chr(ord('A') + i) for i in range(COLS)]
    checker = CHECKERS[player]
    
    while True:
        move = input(f"Player {checker}, please enter a column: ").strip().upper()
        if move in valid_columns:
            col = ord(move) - ord('A')
            # Check if column is full
            if board[0][col] != ' ':
                print("Column is full. Choose another column.")
            else:
                return col
        else:
            print(f"Invalid column. Choose from {', '.join(valid_columns)}.")

def drop_checker(board, col, checker):
    """Drop the checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full (should not happen since checked earlier)

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    checker = board[row][col]
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
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
        # If count >= 4, it's a win
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    print("Starting Connect 4!")
    print_board(board)
    
    while True:
        col = get_player_move(current_player, board)
        row = drop_checker(board, col, CHECKERS[current_player])
        print_board(board)
        
        if check_win(board, row, col):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
