import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print each row with borders
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+' + '---+' * COLS)

def get_random_first_player():
    """Return a random player index to start the game."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(col_input):
    """Check if the column input is valid (a letter within the column range)."""
    if len(col_input) != 1:
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < COLS

def drop_checker(board, col, player_symbol):
    """Drop a checker into the specified column.
    Returns the row where the checker was placed, or -1 if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row
    return -1

def check_win(board, row, col, player_symbol):
    """Check if the last move caused a win (4 in a row horizontally, vertically, or diagonally)."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down
        (1, -1)   # Diagonal up
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        # If 4 in a row, return True
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player()
    player_symbols = PLAYERS[:NUM_PLAYERS]
    
    print(f"Player {player_symbols[current_player]} starts first!")
    
    while True:
        print_board(board)
        current_symbol = player_symbols[current_player]
        
        # Get valid column input from the player
        while True:
            col_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
            if is_valid_column(col_input):
                col = ord(col_input) - ord('A')
                break
            print("Invalid input. Please enter a valid column letter (A to " + chr(65 + COLS - 1) + ").")
        
        # Drop the checker and check if column is full
        row = drop_checker(board, col, current_symbol)
        if row == -1:
            print(f"Column {col_input} is full. Player {current_symbol} loses their turn.")
        else:
            # Check for win
            if check_win(board, row, col, current_symbol):
                print_board(board)
                print(f"Player {current_symbol} won!")
                break
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
