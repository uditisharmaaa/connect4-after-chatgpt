import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print each row with borders
    for row in board:
        print('+' + '---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+' + '---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid (uppercase letter within range)."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col.isalpha() and ord(col) - ord('A') < COLS

def get_column_input(player):
    """Prompt the player for a column input and validate it."""
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if is_valid_column(col):
            return ord(col) - ord('A')
        print("Invalid input. Please enter a valid column letter (A-" + chr(65 + COLS - 1) + ")")

def place_checker(board, col, symbol):
    """Place the player's symbol in the lowest available row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False  # Column is full

def check_win(board, symbol):
    """Check if the current player has won."""
    # Check horizontal, vertical, and both diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == symbol:
                for dr, dc in directions:
                    if is_consecutive_four(board, row, col, dr, dc, symbol):
                        return True
    return False

def is_consecutive_four(board, row, col, dr, dc, symbol):
    """Check if there are four consecutive symbols in a given direction."""
    for _ in range(3):
        row += dr
        col += dc
        if not (0 <= row < ROWS and 0 <= col < COLS and board[row][col] == symbol):
            return False
    return True

def is_draw(board):
    """Check if the game is a draw (no more valid moves)."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    print("Starting Connect 4!")
    print(f"Player {symbols[current_player]} goes first.")
    
    while True:
        print_board(board)
        col = get_column_input(symbols[current_player])
        
        if not place_checker(board, col, symbols[current_player]):
            print("Column is full. You lose your turn.")
        else:
            if check_win(board, symbols[current_player]):
                print_board(board)
                print(f"Player {symbols[current_player]} won!")
                return
            if is_draw(board):
                print_board(board)
                print("Game is a draw!")
                return
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
