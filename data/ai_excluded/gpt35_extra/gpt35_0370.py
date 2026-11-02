import os
import random

# Constants for the game configuration
ROWS = 6           # Number of rows (height)
COLS = 7           # Number of columns (width)
PLAYERS = 2        # Number of players (between 2 and 5)
WIN_COUNT = 4      # Number of checkers in a row needed to win
MAX_PLAYERS = 5    # Maximum players supported
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates and returns a board initialized with spaces.
    Board is a list of lists: board[row][col].
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board to the terminal with column labels.
    """
    clear_screen()
    # Print column labels (A, B, C ...)
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(labels))
    
    # Print the board rows from top to bottom
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def get_valid_columns(board):
    """
    Returns a list of column indices that are not full
    (i.e., columns where a checker can be dropped).
    """
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':  # Top cell empty => column not full
            valid_cols.append(col)
    return valid_cols

def input_column(board, current_player):
    """
    Prompts the current_player to enter a valid column (A-G).
    Validates the input and returns the column index.
    If column is full, player loses turn (return None).
    """
    cols = len(board[0])
    valid_inputs = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_inputs:
            print(f"Invalid input '{col_input}'. Please enter a letter between A and {valid_inputs[-1]}.")
            continue
        col = ord(col_input) - ord('A')
        # Check if column is full
        if board[0][col] != ' ':
            # Column full - player loses turn
            print(f"Column {col_input} is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, checker):
    """
    Places the checker in the specified column in the lowest available row.
    Returns the row where the checker was placed.
    """
    for row in reversed(range(len(board))):  # Start from bottom row
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    # Should never reach here because we check if column is full before
    return None

def check_winner(board, row, col, checker):
    """
    Checks if placing 'checker' at (row, col) creates a winning alignment.
    Winner is identified by 4 in a row in any direction:
    horizontal, vertical, diagonal (\), diagonal (/)
    Returns True if winner found, False otherwise.
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right \
        (1, -1)   # Diagonal down-left /
    ]
    
    rows = len(board)
    cols = len(board[0])
    
    for dr, dc in directions:
        count = 1  # Count includes the placed checker
        
        # Check forward direction (dr, dc)
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
            if count == WIN_COUNT:
                return True
        
        # Check backward direction (-dr, -dc)
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
            if count == WIN_COUNT:
                return True
    return False

def check_draw(board):
    """
    Returns True if the board is full (draw), False otherwise.
    """
    return all(cell != ' ' for cell in board[0])

def main():
    # Validate constants settings (just for safety)
    assert 2 <= PLAYERS <= MAX_PLAYERS, "Number of players must be between 2 and 5"
    assert ROWS > 0 and COLS > 0 and COLS <= 26, "Column count must be between 1 and 26"
    
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select the first player index
    current_player_index = random.randint(0, PLAYERS - 1)
    
    # Print initial empty board
    print_board(board)
    
    while True:
        current_checker = players_checkers[current_player_index]
        
        # Get valid columns
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            # Board full => draw
            print("The board is full. The game is a draw!")
            break
        
        col = input_column(board, current_checker)
        if col is None:
            # Player loses turn due to full column input, continue to next player
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        
        # Place checker in the chosen column
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_winner(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The board is full. The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
