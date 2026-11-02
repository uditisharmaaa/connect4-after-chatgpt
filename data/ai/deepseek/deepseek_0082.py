import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Initialize an empty game board with specified dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the game board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(len(board[0]))]))
    
    # Print the board rows with borders
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_column(col, board):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_upper = col.upper()
    if not col_upper.isalpha():
        return False
    col_index = ord(col_upper) - ord('A')
    return 0 <= col_index < len(board[0])

def place_checker(board, col, symbol):
    """Place a checker in the specified column if possible."""
    col_index = ord(col.upper()) - ord('A')
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = symbol
            return True
    return False  # Column is full

def check_win(board, symbol):
    """Check if the current player has won the game."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == symbol:
                for dr, dc in directions:
                    found = True
                    for step in range(1, 4):
                        r, c = row + dr * step, col + dc * step
                        if (r < 0 or r >= len(board) or 
                            c < 0 or c >= len(board[0]) or 
                            board[r][c] != symbol):
                            found = False
                            break
                    if found:
                        return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        player_symbol = symbols[current_player]
        print(f"Player {player_symbol}, please enter a column: ")
        col_input = input().strip()
        
        if not is_valid_column(col_input, board):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        if not place_checker(board, col_input, player_symbol):
            print("Column is full. You lose this turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        print_board(board)
        
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
