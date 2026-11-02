import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players supported

def initialize_board(rows, cols):
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with columns labeled A, B, C, etc."""
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(headers))
    
    # Print each row with borders
    border = '+' + ('---+' * len(board[0]))
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def get_valid_column(board):
    """Prompt the player for a valid column input."""
    columns = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        col = input(f"Choose a column ({', '.join(columns)}): ").upper()
        if not col:
            print("Please enter a column.")
            continue
        if col[0] not in columns:
            print(f"Invalid column. Use one of {', '.join(columns)}.")
            continue
        col_index = ord(col[0]) - ord('A')
        if board[0][col_index] != ' ':  # Column is full
            print("This column is full. Choose another one.")
            continue
        return col_index

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest available row."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return -1, -1  # Column is full (shouldn't happen if input validated)

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win in any direction."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current position counts as 1
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        os.system('clear')  # Clear the screen
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        # Get valid column input
        col = get_valid_column(board)
        
        # Place the checker
        row, _ = place_checker(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    play_game()
