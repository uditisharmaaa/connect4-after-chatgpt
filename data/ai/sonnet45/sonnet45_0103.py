import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checker symbols
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and grid lines."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print horizontal divider
    print('  ' + '+---' * COLS + '+')
    
    # Print each row
    for row in range(ROWS):
        print('  ', end='')
        for col in range(COLS):
            print(f'| {board[row][col]} ', end='')
        print('|')
        print('  ' + '+---' * COLS + '+')


def is_valid_column(board, col):
    """Check if a column index is valid and has space available."""
    if col < 0 or col >= COLS:
        return False
    # Check if the top row of the column is empty
    return board[0][col] == ' '


def get_next_row(board, col):
    """Get the next available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1


def place_checker(board, col, symbol):
    """Place a checker in the specified column and return the row it was placed in."""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = symbol
    return row


def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) created a winning condition."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    # Check diagonal
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find starting position of diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    # Check diagonal
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def get_player_input(board, player_symbol):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column has space
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Set up players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        col = get_player_input(board, current_player)
        
        # Place checker
        row = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
