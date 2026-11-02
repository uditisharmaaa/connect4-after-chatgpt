import random
import os

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print board rows with borders
    for row in range(ROWS):
        # Print top border of row
        print('  +' + '---+' * COLS)
        
        # Print row content
        print('  |', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print('  +' + '---+' * COLS)


def get_valid_move(board, player_checker):
    """Get a valid column choice from the player."""
    while True:
        move = input(f'Player {player_checker}, please enter a column: ').strip().upper()
        
        # Check if input is a single character
        if len(move) != 1:
            print('Invalid input. Please enter a single column letter.')
            continue
        
        # Check if input is a letter
        if not move.isalpha():
            print('Invalid input. Please enter a letter.')
            continue
        
        # Convert letter to column index
        col_index = ord(move) - 65
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLS:
            print(f'Invalid column. Please choose between A and {chr(64 + COLS)}.')
            continue
        
        # Check if column has available space
        if board[0][col_index] != ' ':
            print('Column is full. Please choose another column.')
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """Place a checker in the specified column. Returns the row where it was placed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_checker
            return row
    return -1


def check_win(board, row, col, player_checker):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
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
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
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
        
        # Get valid move from player
        col = get_valid_move(board, current_player)
        
        # Place checker
        row = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f'Player {current_player} won!')
            break
        
        # Check for draw
        if check_draw(board):
            print('The game is a draw!')
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == '__main__':
    play_game()
