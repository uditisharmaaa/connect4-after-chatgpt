import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_CONDITION = 4

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print board rows
    for row in board:
        line = '+---' * COLS + '+'
        print(line)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---' * COLS + '+')

def get_valid_column_input(current_player):
    """Get valid column input from the current player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
            col = ord(col_input) - ord('A')
            return col
        else:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")

def place_checker(board, col, checker):
    """Place a checker in the specified column if possible."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    # Directions: (row, col) increments for up, down, left, right, and diagonals
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if win condition is met
        if count >= WIN_CONDITION:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        col = get_valid_column_input(current_player)
        row = place_checker(board, col, current_player)
        
        if row == -1:
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, row, col, current_player):
                os.system('clear')
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                os.system('clear')
                print_board(board)
                print("Game is a draw!")
                break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
