import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of possible checker symbols in order
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows with borders
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---+' * COLS)

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if len(col) != 1 or not col.isalpha():
        return False
    
    col_index = ord(col.upper()) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if the column has at least one empty space
    return board[0][col_index] == ' '

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest available row."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal, vertical, and both diagonal directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                for dr, dc in directions:
                    count = 1
                    for step in range(1, 4):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = CHECKER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    print("Welcome to Connect 4!")
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ", end='')
        col = input().strip().upper()
        
        if not is_valid_column(col, board):
            print("Invalid input. Please enter a valid column (A to G).")
            continue
        
        # Place the checker and switch player if successful
        if place_checker(board, col, current_player):
            print_board(board)
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if is_draw(board):
                print("Game over! It's a draw.")
                break
            
            # Switch to the next player
            current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
