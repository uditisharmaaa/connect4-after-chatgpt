import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player tokens in order
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print row contents
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def get_random_first_player():
    """Return a random player index to start the game."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(65 + COLS - 1)

def get_player_input(player_token):
    """Get and validate player input for column choice."""
    while True:
        col = input(f"Player {player_token}, please enter a column: ").upper()
        if is_valid_column(col):
            return ord(col) - ord('A')
        print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")

def place_checker(board, col, player_token):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return True
    return False  # Column is full

def check_win(board, player_token):
    """Check if the player has won with 4 in a row (horizontally, vertically, diagonally)."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_token for i in range(4)):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player_token for i in range(4)):
                return True
    
    # Check diagonally (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_token for i in range(4)):
                return True
    
    # Check diagonally (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_token for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player()
    player_tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        player_token = player_tokens[current_player]
        col = get_player_input(player_token)
        
        if not place_checker(board, col, player_token):
            print(f"Column {chr(65 + col)} is full. Player {player_token} loses their turn.")
        else:
            print_board(board)
            if check_win(board, player_token):
                print(f"Player {player_token} won!")
                break
            if is_draw(board):
                print("Game ended in a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
