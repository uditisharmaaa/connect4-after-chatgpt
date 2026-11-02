import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Tokens based on number of players

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def get_random_first_player():
    """Randomly select the first player."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column_input(col_input):
    """Check if the column input is valid (a letter within the board's columns)."""
    if len(col_input) != 1:
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < COLS

def get_valid_column_input(player_idx):
    """Prompt the player for a column input until a valid one is provided."""
    while True:
        col_input = input(f"Player {PLAYER_TOKENS[player_idx]}, please enter a column: ").strip().upper()
        if is_valid_column_input(col_input):
            col = ord(col_input) - ord('A')
            return col
        print("Invalid input. Please enter a valid column letter (A to {}).".format(chr(65 + COLS - 1)))

def place_checker(board, col, token):
    """Place the player's token in the lowest available row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row  # Return the row where the token was placed
    return -1  # Column is full

def check_win(board, row, col, token):
    """Check if the player has won (4 in a row horizontally, vertically, or diagonally)."""
    # Directions: (dr, dc) for checking in 4 directions (horizontal, vertical, 2 diagonals)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current token
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (no empty spaces)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = get_random_first_player()
    
    while True:
        os.system('clear')
        print_board(board)
        
        col = get_valid_column_input(current_player)
        row = place_checker(board, col, PLAYER_TOKENS[current_player])
        
        if row == -1:
            print("Column is full. You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, row, col, PLAYER_TOKENS[current_player]):
                os.system('clear')
                print_board(board)
                print(f"Player {PLAYER_TOKENS[current_player]} won!")
                break
            if is_board_full(board):
                os.system('clear')
                print_board(board)
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
