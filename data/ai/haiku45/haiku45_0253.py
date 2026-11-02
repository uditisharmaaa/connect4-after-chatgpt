import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """Create and return an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column(col, cols):
    """Check if column is valid (0-indexed)."""
    return 0 <= col < cols


def is_column_full(board, col):
    """Check if a column is completely filled."""
    return board[0][col] != " "


def place_checker(board, col, checker):
    """Place checker in column and return row if successful, -1 otherwise."""
    if is_column_full(board, col):
        return -1
    
    # Find lowest empty row in column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def get_player_move(num_cols, current_player, checkers):
    """Get valid column input from player."""
    while True:
        try:
            user_input = input(f"Player {checkers[current_player]}, please enter a column: ").strip().upper()
            
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col = ord(user_input) - ord('A')
            
            if not is_valid_column(col, num_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(65 + num_cols - 1)}.")
                continue
            
            return col
        except Exception:
            print("Invalid input. Please try again.")


def check_winner(board, row, col, checker):
    """Check if the last placed checker creates a win."""
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the placed checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if board is completely filled (draw condition)."""
    return all(board[0][col] != " " for col in range(len(board[0])))


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checkers = CHECKERS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        col = get_player_move(COLS, current_player, checkers)
        
        row = place_checker(board, col, checkers[current_player])
        
        if row == -1:
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        print_board(board)
        
        if check_winner(board, row, col, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
