import random
import os

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for i in range(COLS):
        print(f'  {chr(65 + i)} ', end='')
    print()
    
    # Print board rows
    for row in range(ROWS):
        # Print horizontal separator
        print('  ', end='')
        for _ in range(COLS):
            print('+---', end='')
        print('+')
        
        # Print row content
        print('  ', end='')
        for col in range(COLS):
            print(f'| {board[row][col]} ', end='')
        print('|')
    
    # Print bottom border
    print('  ', end='')
    for _ in range(COLS):
        print('+---', end='')
    print('+')


def get_valid_column(board, player):
    """Get a valid column input from the player."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip()
        
        # Check if input is a single character
        if len(col_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not col_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase and get column index
        col_letter = col_input.upper()
        col_index = ord(col_letter) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != ' ':
            print("Column is full. You lose your turn.")
            return -1
        
        return col_index


def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
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
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
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
            if count == WIN_COUNT:
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
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def play_game():
    """Main game loop."""
    # Initialize game
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input
        col = get_valid_column(board, current_player)
        
        # If column is full, skip to next player
        if col == -1:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        row = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
