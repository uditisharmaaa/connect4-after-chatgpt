import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for i in range(COLS):
        print(f'  {chr(65 + i)} ', end='')
    print()
    
    # Print board rows
    for row in board:
        print('+' + '---+' * COLS)
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+' + '---+' * COLS)

def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column index is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False
    
    return True

def place_checker(board, col_letter, symbol):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = symbol
            return row, col_index
    
    return None, None

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_input(player_symbol, board):
    """Get and validate player input."""
    while True:
        col_letter = input(f"Player {player_symbol}, please enter a column: ").upper()
        
        if is_valid_column(col_letter, board):
            return col_letter
        else:
            print("Invalid input. Please try again.")

def main():
    """Main game loop."""
    # Create board
    board = create_board()
    
    # Set up players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        col_letter = get_player_input(current_player, board)
        
        # Place checker
        row, col = place_checker(board, col_letter, current_player)
        
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
    main()
