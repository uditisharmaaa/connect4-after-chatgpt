import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First N players based on NUM_PLAYERS

def initialize_board():
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def get_valid_column(player):
    """Prompt the player to enter a column and validate the input."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(col_input) - ord('A')
        if 0 <= col < BOARD_COLS:
            return col
        print(f"Invalid column. Please enter a letter from A to {chr(65 + BOARD_COLS - 1)}.")

def place_checker(board, col, player):
    """
    Place the player's checker in the specified column.
    Returns the row where the checker was placed, or -1 if the column is full.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Column is full

def check_win(board, row, col, player):
    """Check if the player has won after placing a checker at (row, col)."""
    # Directions: (dx, dy) for horizontal, vertical, and two diagonals
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # current (row, col) is already counted
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
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
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(current_player)
        row = place_checker(board, col, current_player)
        
        if row == -1:
            print("This column is full. You lose your turn.")
        else:
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
        print_board(board)

if __name__ == "__main__":
    play_game()
