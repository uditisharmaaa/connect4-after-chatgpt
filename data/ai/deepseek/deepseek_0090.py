import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First N players from the list

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the board rows with borders
    border = '+' + ('---+' * COLS)
    print(border)
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(border)

def is_valid_move(board, col):
    """Check if a move is valid (column is within bounds and not full)."""
    return 0 <= col < COLS and board[0][col] == ' '

def make_move(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won by getting 4 in a row (horizontally, vertically, diagonally)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw (no more valid moves)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_input(player):
    """Get and validate player input for column choice."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            if len(col_input) != 1:
                print("Invalid input. Please enter a single letter (A-G).")
                continue
            col = ord(col_input) - ord('A')
            if 0 <= col < COLS:
                return col
            else:
                print(f"Invalid column. Please enter a letter between A-{chr(ord('A') + COLS - 1)}.")
        except ValueError:
            print("Invalid input. Please enter a valid letter.")

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_player_input(current_player)
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        make_move(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
