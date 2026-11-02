import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']  # Ordered list of player characters

def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def is_valid_column(col, board):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_char = col[0].upper()
    return col_char >= 'A' and ord(col_char) < ord('A') + len(board[0])

def get_column_index(col):
    """Convert the column character to an index."""
    return ord(col[0].upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Attempt to place the checker in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    col_index = get_column_index(col)
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has a winning line."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontally
    for row in range(rows):
        for col in range(cols - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertically
    for row in range(rows - 3):
        for col in range(cols):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonally (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonally (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled with checkers."""
    for row in board:
        if ' ' in row:
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYER_CHARS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        clear_screen()
        print_board(board)
        
        print(f"Player {current_player}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input, board):
            continue
        
        col_index = get_column_index(col_input)
        if not place_checker(board, col_input, current_player):
            continue  # Column is full, try again
        
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % len(players)]

if __name__ == "__main__":
    main()
