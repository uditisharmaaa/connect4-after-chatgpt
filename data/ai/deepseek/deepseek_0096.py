import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def is_valid_column(col, board):
    """Check if the column is valid and not full."""
    if len(col) != 1:
        return False
    col_idx = ord(col.upper()) - ord('A')
    if 0 <= col_idx < COLS:
        return board[0][col_idx] == ' '
    return False

def drop_checker(board, col, checker):
    """Place the checker in the specified column and return the row position."""
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1  # The current position is already a match
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
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print_board(board)
    
    while True:
        # Get player input
        while True:
            col = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if is_valid_column(col, board):
                break
            print("Invalid input. Please try again.")
        
        # Drop the checker and get the row position
        row = drop_checker(board, col, current_player)
        print_board(board)
        
        # Check for win
        if check_win(board, row, ord(col) - ord('A'), current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
