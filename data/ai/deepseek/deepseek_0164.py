import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with whitespaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the board rows
    horizontal_divider = '+' + '---+' * COLS
    print(horizontal_divider)
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(horizontal_divider)

def get_valid_column(board):
    """Prompt the player for a column input and validate it."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not col_input.isalpha():
            print("Invalid input. Please enter a letter (A-{}).".format(chr(65 + COLS - 1)))
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print("Column out of range. Please enter a letter from A to {}.".format(chr(65 + COLS - 1)))
            continue
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
