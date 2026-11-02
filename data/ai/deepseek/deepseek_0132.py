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
    """Print the current state of the game board with column labels."""
    # Clear the screen before printing the board
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+' + '---+' * COLS)

def get_valid_column(board):
    """Prompt the current player to select a column until a valid input is provided."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        
        # Check if input is a single uppercase letter
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col = ord(col_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def drop_checker(board, col, player):
    """Place the player's checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win for the player."""
    # Directions: horizontal, vertical, diagonal up, diagonal down
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current cell is already the player's
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full (a draw)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    board = initialize_board()
    global current_player
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row = drop_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
