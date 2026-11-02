import os
import random

# Constants
COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board to the console."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print board
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def place_checker(board, col, checker):
    """Place a checker in the given column and return the row it was placed in."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if placing a checker at (row, col) results in a win."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, current_player):
    """Get a valid column input from the current player."""
    while True:
        try:
            col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
            if len(col_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            col = ord(col_input) - ord('A')
            if not is_valid_move(board, col):
                print("Invalid move. Column is out of bounds or full.")
                continue
            return col
        except:
            print("Invalid input. Please enter a letter.")

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    print(f"Game starts! Player {CHECKERS[current_player]} goes first.\n")
    
    while True:
        # Get player move
        col = get_player_move(board, current_player)
        row = place_checker(board, col, CHECKERS[current_player])
        
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
