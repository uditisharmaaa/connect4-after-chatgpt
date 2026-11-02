import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print(' ', end=' ')
    for i in range(COLS):
        print(f' {chr(65 + i)} ', end=' ')
    print()
    
    # Print each row with borders
    for row in board:
        print('+' + '---+' * COLS)
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+' + '---+' * COLS)

def is_valid_column(col_input, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_input.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_input) - ord('A')
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False
    
    return True

def place_checker(board, col_input, player_char):
    """Place a checker in the specified column."""
    col_index = ord(col_input) - ord('A')
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player_char
            return row, col_index
    
    return -1, -1

def check_win(board, row, col, player_char):
    """Check if the current player has won."""
    # Check horizontal
    if check_direction(board, row, col, player_char, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player_char, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player_char, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, player_char, -1, 1):
        return True
    
    return False

def check_direction(board, row, col, player_char, row_dir, col_dir):
    """Check if there are 4 in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + row_dir, col + col_dir
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_char:
        count += 1
        r += row_dir
        c += col_dir
    
    # Check in negative direction
    r, c = row - row_dir, col - col_dir
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_char:
        count += 1
        r -= row_dir
        c -= col_dir
    
    return count >= WIN_LENGTH

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = [PLAYER_CHARS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column: ", end='')
        col_input = input().strip()
        
        # Validate input
        while not is_valid_column(col_input, board):
            print("Invalid input. Please enter a valid column: ", end='')
            col_input = input().strip()
        
        # Place checker
        row, col = place_checker(board, col_input, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
