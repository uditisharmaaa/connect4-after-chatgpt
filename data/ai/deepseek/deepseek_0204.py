import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with the specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the board with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
    print(border)

def is_valid_column(col):
    """Check if the input column is valid (a letter within the board's columns)."""
    if len(col) != 1:
        return False
    return col.isalpha() and ord(col.upper()) - ord('A') < COLS

def get_next_open_row(board, col):
    """Find the lowest empty row in the specified column."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            return row
    return -1  # Column is full

def drop_checker(board, row, col, player):
    """Place the player's checker in the specified position."""
    col_index = ord(col.upper()) - ord('A')
    board[row][col_index] = player

def check_win(board, player):
    """Check if the specified player has a winning combination."""
    # Check horizontal, vertical, and both diagonals
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + i * dr, col + i * dc
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    clear_screen()
    print(f"Player {current_player} starts the game!")
    print_board(board)
    
    while True:
        while True:
            col = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if not is_valid_column(col):
                print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
                continue
            
            row = get_next_open_row(board, col)
            if row == -1:
                print("Column is full. Try another column.")
                continue
            break
        
        drop_checker(board, row, col, current_player)
        clear_screen()
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("Game over. It's a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
