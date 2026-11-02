import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    
    # Print the board rows with borders
    border = '+' + ('---+' * COLUMNS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def is_valid_column(column):
    """Check if the input column is valid."""
    if len(column) != 1:
        return False
    column_upper = column.upper()
    return column_upper.isalpha() and ord(column_upper) - ord('A') < COLUMNS

def place_checker(board, column, symbol):
    """
    Place the symbol in the lowest available row of the specified column.
    Returns the row index where the symbol was placed, or -1 if the column is full.
    """
    col_idx = ord(column.upper()) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = symbol
            return row_idx
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (no more valid moves)."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    """Main function to play the Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:PLAYERS]
    
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {symbols[current_player]}, please enter a column:")
        
        while True:
            column = input().strip()
            if is_valid_column(column):
                col_upper = column.upper()
                row = place_checker(board, col_upper, symbols[current_player])
                if row != -1:
                    break
                print("Column is full. Please choose another column.")
            else:
                print(f"Invalid input. Please enter a letter from A to {chr(65 + COLUMNS - 1)}.")
        
        if check_win(board, row, ord(col_upper) - ord('A'), symbols[current_player]):
            os.system('clear')
            print_board(board)
            print(f"Player {symbols[current_player]} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
