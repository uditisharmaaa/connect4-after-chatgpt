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
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print(' ', end=' ')
    for col in range(COLS):
        print(f' {chr(65 + col)} ', end=' ')
    print()
    
    # Print horizontal divider
    print('+' + '---+' * COLS)
    
    # Print each row
    for row in range(ROWS):
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
        print('+' + '---+' * COLS)


def is_valid_column(column_input):
    """Check if the column input is a valid letter within board range."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    col_index = ord(column_input.upper()) - ord('A')
    return 0 <= col_index < COLS


def is_column_full(board, col_index):
    """Check if the specified column is full."""
    return board[0][col_index] != ' '


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
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
        if board[r][c] == checker:
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
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def get_valid_move(board, player_checker):
    """Get a valid column input from the player."""
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is valid
        if not is_valid_column(move):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(move) - ord('A')
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid move from player
        col_index = get_valid_move(board, checker)
        
        # Place checker
        row_index = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
