import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Player checkers in order
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board with column headers and borders."""
    # Print column headers (A, B, C, ...)
    headers = '   ' + '   '.join([chr(65 + i) for i in range(len(board[0]))])
    print(headers)
    
    # Print top border
    border = '+' + ('---+' * len(board[0]))
    print(border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(border)

def get_valid_column():
    """Prompt the current player for a column and validate the input."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= NUM_COLS:
            print(f"Column must be between A and {chr(ord('A') + NUM_COLS - 1)}.")
            continue
        return col

def drop_checker(board, col, checker):
    """Drop a checker in the specified column and return the row where it lands."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None  # Column is full

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
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
        while (0 <= r < len(board) and 0 <= c < len(board[0]) and 
               board[r][c] == checker):
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while (0 <= r < len(board) and 0 <= c < len(board[0]) and 
               board[r][c] == checker):
            count += 1
            r -= dr
            c -= dc
        # If 4 or more in a line, return True
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (no empty spaces)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def play_game():
    """Main game loop."""
    global current_player
    board = initialize_board(NUM_ROWS, NUM_COLS)
    current_player = random.choice(range(NUM_PLAYERS))
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    while True:
        clear_screen()
        print_board(board)
        col = get_valid_column()
        row = drop_checker(board, col, checkers[current_player])
        
        if row is None:
            print("Column is full. Lost your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        if check_win(board, row, col, checkers[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
