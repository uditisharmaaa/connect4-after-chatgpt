import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * NUM_COLS)
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def get_valid_column(player, board):
    """Prompt the player for a column input and validate it."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if not col_input or len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= NUM_COLS:
            print(f"Column must be between A and {chr(65 + NUM_COLS - 1)}.")
            continue
        
        if board[0][col] != ' ':
            print("Column is full. Choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column at the lowest empty row."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the player has won after placing a checker at (row, col)."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1  # current (row, col) is already counted
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        col = get_valid_column(current_player, board)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch players
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
