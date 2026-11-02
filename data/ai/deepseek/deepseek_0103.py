import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Default checkers for up to 5 players

def initialize_board():
    """Initialize a blank game board with specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')
    # Print column headers
    headers = [chr(65 + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print each row
    for row in board:
        border = '+'.join(['---'] * BOARD_COLS)
        print('+' + border + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    border = '+'.join(['---'] * BOARD_COLS)
    print('+' + border + '+')

def is_valid_column(col_input):
    """Check if the input is a valid column letter."""
    if len(col_input) != 1:
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < BOARD_COLS

def place_checker(board, col, checker):
    """
    Place the checker in the specified column.
    Returns the row where the checker was placed, or -1 if the column is full.
    """
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # If 4 in a row, return True
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {PLAYERS[current_player]} starts first.")
    
    while True:
        # Get valid column input
        while True:
            col_input = input(f"Player {PLAYERS[current_player]}, please enter a column: ").strip().upper()
            if is_valid_column(col_input):
                col = ord(col_input) - ord('A')
                break
            else:
                print("Invalid input. Please enter a valid column letter (A-" + chr(ord('A') + BOARD_COLS - 1) + ").")
        
        # Place checker
        row = place_checker(board, col, PLAYERS[current_player])
        if row == -1:
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        # Check win
        if check_win(board, row, col, PLAYERS[current_player]):
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        # Check draw
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
