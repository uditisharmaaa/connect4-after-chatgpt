import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create and initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end=" ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")

def get_valid_column(board, cols, player_checker):
    """Get valid column input from player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if user_input < 'A' or user_input >= chr(ord('A') + cols):
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        col = ord(user_input) - ord('A')
        
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place checker in the lowest available space in the column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker, rows, cols):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board, COLS)
    
    while True:
        col = get_valid_column(board, COLS, checkers[current_player])
        row = place_checker(board, col, checkers[current_player])
        
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row, col, checkers[current_player], ROWS, COLS):
            print(f"Player {checkers[current_player]} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
