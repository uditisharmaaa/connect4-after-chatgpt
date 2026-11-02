import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + ('---+' * COLS))
    # Print each row with borders
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def get_random_first_player():
    """Return a random player index to start the game."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(column):
    """Check if the column input is valid (a letter within the column range)."""
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def place_checker(board, col, checker):
    """
    Place a checker in the specified column if possible.
    Returns the row where the checker was placed, or -1 if the column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """
    Check if the last placed checker results in a win.
    Win conditions: 4 in a row horizontally, vertically, or diagonally.
    """
    # Directions: horizontal, vertical, diagonal down-right, diagonal up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1  # current checker is already placed
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
    """Check if the game is a draw (all spaces filled)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player()
    clear_screen()
    print_board(board)

    while True:
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter (A-" + chr(65 + COLS - 1) + ").")
            continue
        
        col = ord(column) - ord('A')
        row = place_checker(board, col, checker)
        
        if row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("Game over. It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
