import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS))
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print(border)

def get_valid_column(board, player):
    """Prompt the player for a column and validate the input."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A-Z).")
            continue
        
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        if board[0][col_index] != ' ':
            print("This column is already full. Please choose another one.")
            continue
        
        return col_index

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the player has won after placing a checker."""
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
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_valid_column(board, current_player)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
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
    main()
