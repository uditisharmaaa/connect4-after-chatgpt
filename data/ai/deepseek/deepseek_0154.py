import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]  # Slice to get required symbols

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column letters
    print("  " + "   ".join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print top border
    border = "+" + ("---+" * BOARD_COLS)
    print(border)
    
    # Print each row with borders
    for row in board:
        print("| " + " | ".join(cell for cell in row) + " |")
        print(border)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def get_valid_column():
    """Get valid column input from the player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Check if input is a single uppercase letter and within board range
        if len(col_input) != 1:
            print("Invalid input. Please enter a single column letter (A to G).")
            continue
            
        col = ord(col_input) - ord('A')
        
        if col < 0 or col >= BOARD_COLS:
            print(f"Invalid column. Please choose between A to {chr(65 + BOARD_COLS - 1)}.")
            continue
            
        # Check if column is not full
        if board[0][col] != " ":
            print("Column is full. Choose another column.")
            continue
            
        return col

def place_checker(col):
    """Place the checker in the lowest available row of the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = current_player
            return row
    return -1  # Should not reach here if input validated

def check_win(row, col):
    """Check if the current move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Current cell
        
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == current_player:
            count += 1
            r += dr
            c += dc
        
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == current_player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
            
    return False

def is_draw():
    """Check if the board is full (draw)."""
    return all(cell != " " for cell in board[0])

def switch_player():
    """Switch to the next player."""
    global current_player, current_player_idx
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
    current_player = PLAYER_SYMBOLS[current_player_idx]

# Initialize game
board = initialize_board()
current_player_idx = random.randint(0, NUM_PLAYERS - 1)
current_player = PLAYER_SYMBOLS[current_player_idx]
game_over = False

# Main game loop
while not game_over:
    clear_screen()
    print_board(board)
    
    # Get valid column input and place checker
    col = get_valid_column()
    row = place_checker(col)
    
    # Check for win or draw
    if check_win(row, col):
        clear_screen()
        print_board(board)
        print(f"Player {current_player} won!")
        game_over = True
    elif is_draw():
        clear_screen()
        print_board(board)
        print("It's a draw!")
        game_over = True
    else:
        switch_player()
