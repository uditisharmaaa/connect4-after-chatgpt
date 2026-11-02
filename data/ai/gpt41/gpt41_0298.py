import os
import random
import string

# ----------- CONSTANT VARIABLES (Change as needed) -------------
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Change to 2..5 for multiple players
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

# ----------- UTILITY FUNCTIONS -------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a board filled with ' ' (space)."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    rows = len(board)
    cols = len(board[0])

    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    
    # Print the lines
    print('+' + '---+' * cols)
    
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print('+' + '---+' * cols)

def get_available_row(board, col):
    """
    Returns the index of the lowest available row in the specified column.
    Returns -1 if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return -1

def is_valid_column(input_col, cols):
    """
    Checks if the input is a valid column letter within the range A-G/etc.
    """
    if len(input_col) != 1:
        return False
    col_index = ord(input_col) - ord('A')
    return 0 <= col_index < cols

def board_full(board):
    """Returns True if the board is completely full."""
    return all(cell != ' ' for row in board for cell in row)

def check_win(board, row, col, token):
    """
    Checks if placing token at (row, col) causes a win (4 in a row)
    horizontally, vertically, or diagonally.
    Returns True if win detected.
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # including itself
        # Go in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # Go in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# ----------- MAIN GAME LOGIC --------------

def main():
    # Ensure settings are within constraints
    if NUM_COLS > 26 or NUM_COLS < 1:
        print("Maximum 26 columns (A-Z) and at least 1 column supported.")
        return
    if NUM_ROWS < 1:
        print("Board must have at least 1 row.")
        return
    if not (2 <= NUM_PLAYERS <= 5):
        print("Number of players must be in range 2-5.")
        return
    
    # Initialize board
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select tokens only for the number of players
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    
    # Random starting player
    current_idx = random.randrange(NUM_PLAYERS)
    current_player = players[current_idx]
    
    # Show empty board at the start
    clear_screen()
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        input_col = input().strip().upper()

        # Validate input
        if not is_valid_column(input_col, NUM_COLS):
            print(f"Invalid input! Please enter a letter from A to {chr(ord('A')+NUM_COLS-1)}.")
            continue
        
        col_index = ord(input_col) - ord('A')
        row_index = get_available_row(board, col_index)

        # Check for filled up column
        if row_index == -1:
            print(f"Column {input_col} is full! Turn lost.")
            # Player loses turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            current_player = players[current_idx]
            clear_screen()
            print_board(board)
            continue
        
        # Place checker
        board[row_index][col_index] = current_player
        
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_player):
            print(f"Player {current_player} won!")
            break
        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS
        current_player = players[current_idx]

if __name__ == "__main__":
    main()
