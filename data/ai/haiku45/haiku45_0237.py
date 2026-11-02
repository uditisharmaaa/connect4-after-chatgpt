import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def get_valid_input(board, players, current_player):
    """Get and validate player input, return column index."""
    while True:
        try:
            col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            
            if len(col_input) != 1 or col_input < 'A' or col_input >= chr(65 + COLS):
                print("Invalid column. Please enter a valid column letter.")
                continue
            
            col = ord(col_input) - 65
            
            if board[0][col] != " ":
                print("Column is full. Please choose another column.")
                continue
            
            return col
        except:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, player):
    """Place checker in the column, return row index or -1 if invalid."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[player]
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    checker = CHECKERS[player]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        col = get_valid_input(board, NUM_PLAYERS, current_player)
        row = place_checker(board, col, current_player)
        
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
