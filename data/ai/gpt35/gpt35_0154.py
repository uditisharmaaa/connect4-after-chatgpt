import os
import random

# Constants for the game
ROWS = 6            # Number of rows in the board
COLUMNS = 7         # Number of columns in the board
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2     # Number of players for submission (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players, support up to 5 players
WIN_COUNT = 4       # Number of consecutive checkers needed to win

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Create a board initialized with spaces.
    
    Args:
    rows (int): number of rows
    columns (int): number of columns
    
    Returns:
    list: 2D list representing the board
    """
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Print the current state of the board with column labels.
    
    Args:
    board (list): 2D list representing the board
    """
    clear_screen()
    # Print column headers (A, B, C, ...)
    column_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(column_labels))
    
    # Print separator and board cells row by row
    row_count = len(board)
    col_count = len(board[0])
    horizontal_line = '+' + '---+' * col_count
    for row in range(row_count):
        print(horizontal_line)
        # Print each cell in the row with vertical separators
        row_cells = '|'.join(f' {board[row][col]} ' for col in range(col_count))
        print(f'|{row_cells}|')
    print(horizontal_line)

def get_valid_column_input(player_checker, columns, board):
    """
    Prompt the current player for a column input repeatedly until it is valid.
    Invalid inputs include out of range letters, non-letters, and columns full.
    
    Args:
    player_checker (str): current player's checker symbol
    columns (int): number of columns on the board
    board (list): current board state
    
    Returns:
    int or None: the valid column index chosen, or None if no moves possible
    """
    valid_columns = [chr(ord('A') + i) for i in range(columns)]
    
    while True:
        user_input = input(f'Player {player_checker}, please enter a column: ').strip().upper()
        
        # Validate input is a single character and a valid column letter
        if len(user_input) != 1 or user_input not in valid_columns:
            print("Invalid input: please enter a valid column letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        # Check if column is full
        if board[0][col_index] != ' ':
            # If full, player loses turn (indicate and return None)
            print("Column is full. You lose your turn.")
            return None
        
        return col_index

def place_checker(board, col_index, checker):
    """
    Place the checker in the lowest available position in the selected column.
    
    Args:
    board (list): the game board
    col_index (int): the index of the column chosen
    checker (str): the player's checker symbol
    
    Returns:
    tuple: (row_index, col_index) where checker is placed
    """
    # Start from bottom row to top row to find the empty slot
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return (row, col_index)
    # Should not reach here if we check for full columns before placing
    return None

def check_win(board, checker, row, col):
    """
    Check if placing 'checker' at (row,col) creates a winning line of 4.
    
    Args:
    board (list): the game board
    checker (str): player's checker symbol
    row (int): row index where checker was placed
    col (int): column index where checker was placed
    
    Returns:
    bool: True if player wins, False otherwise
    """
    def count_direction(delta_row, delta_col):
        """
        Count consecutive checkers matching 'checker' from (row, col) in one direction.
        """
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count
    
    # Directions: horizontal, vertical, diagonal '\', diagonal '/'
    directions = [
        ((0, 1), (0, -1)),   # horizontal
        ((1, 0), (-1, 0)),   # vertical
        ((1, 1), (-1, -1)),  # diagonal \
        ((1, -1), (-1, 1)),  # diagonal /
    ]

    for dir1, dir2 in directions:
        count = 1  # Count the placed checker itself
        count += count_direction(*dir1)
        count += count_direction(*dir2)
        if count >= WIN_COUNT:
            return True

    return False

def is_board_full(board):
    """
    Check if the board is completely full (no spaces).
    
    Args:
    board (list): the game board
    
    Returns:
    bool: True if full, False otherwise
    """
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Validate NUM_PLAYERS is within valid range
    if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f'Invalid number of players. Must be between {MIN_PLAYERS} and {MAX_PLAYERS}.')
        return
    
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board and starting player info
    print_board(board)
    
    # Game loop
    while True:
        player_checker = players_checkers[current_player_idx]
        
        col_index = get_valid_column_input(player_checker, COLUMNS, board)
        
        # If col_index is None, player loses turn, move to next player
        if col_index is None:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        # Place checker and get position
        row_placed, col_placed = place_checker(board, col_index, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, player_checker, row_placed, col_placed):
            print(f'Player {player_checker} won!')
            break
        
        # Check for draw (board full)
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
