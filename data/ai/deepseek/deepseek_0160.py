import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    
    print('+---' * COLS + '+')

def is_valid_column(column):
    """Check if the column input is valid (A, B, ..., up to max column)."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return col_char >= 'A' and col_char <= chr(65 + COLS - 1)

def get_valid_column(current_player):
    """Prompt the current player for a valid column input."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if is_valid_column(column):
            return ord(column) - ord('A')
        print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")

def place_checker(board, col, player):
    """Place the player's checker in the specified column if possible."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won (4 in a row horizontally, vertically, or diagonally)."""
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
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_valid_column(current_player)
        
        if place_checker(board, col, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
            # Switch to next player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
        else:
            print("Column is full. You lose your turn.")
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
