import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of possible player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---+' * COLS)

def get_player_checkers(num_players):
    """Get the list of player checkers based on number of players."""
    return CHECKERS[:num_players]

def get_random_first_player(num_players):
    """Randomly select the first player."""
    return random.randint(0, num_players - 1)

def is_valid_column(col_input):
    """Check if the column input is valid."""
    if len(col_input) != 1:
        return False
    col_char = col_input.upper()
    return 'A' <= col_char <= chr(ord('A') + COLS - 1)

def get_column_index(col_input):
    """Convert column letter to a 0-based index."""
    return ord(col_input.upper()) - ord('A')

def is_column_full(board, col_index):
    """Check if the specified column is full."""
    return board[0][col_index] != ' '

def drop_checker(board, col_index, checker):
    """Drop a checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True

    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    players = get_player_checkers(NUM_PLAYERS)
    current_player = get_random_first_player(NUM_PLAYERS)
    
    print(f"Player {players[current_player]} goes first!")
    input("Press Enter to start...")
    
    while True:
        print_board(board)
        checker = players[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        col_input = input().strip()
        
        # Validate input
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A-G).")
            input("Press Enter to continue...")
            continue
        
        col_index = get_column_index(col_input)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print(f"Column {col_input} is full. Player {checker} loses this turn!")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place the checker
        drop_checker(board, col_index, checker)
        
        # Check for win
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
