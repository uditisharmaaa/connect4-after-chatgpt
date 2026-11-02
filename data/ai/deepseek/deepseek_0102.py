import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Create an empty board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def get_valid_column(board, player):
    """Ask the player for a column and validate the input."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1:
            print("Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        if board[0][col] != ' ':
            print("That column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonally (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize game
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_index]
    
    while True:
        print_board(board)
        col = get_valid_column(board, current_player)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
