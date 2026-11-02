import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']

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
    for row in range(ROWS):
        print('+' + '---+' * COLS)
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    print('+' + '---+' * COLS)

def get_valid_input(player_checker):
    """Get valid column input from player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        # Check if input is empty
        if len(user_input) == 0:
            print("Invalid input. Please enter a column letter.")
            continue
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if column is within board range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
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

def play_game():
    """Main game loop."""
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        
        # Get valid column input
        col = get_valid_input(current_checker)
        
        # Place checker
        row = place_checker(board, col, current_checker)
        
        # Check if column was full
        if row == -1:
            print(f"Column {chr(65 + col)} is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
