import os
import random

# Constants
COLUMNS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def create_board(rows, cols):
    """Create an empty board with specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)} ", end=" ")
    print()
    
    # Print board rows
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def get_valid_input(board, cols, current_player):
    """Get valid column input from player."""
    while True:
        try:
            user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            
            # Validate input
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col_index = ord(user_input) - ord('A')
            
            if col_index < 0 or col_index >= cols:
                print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
                continue
            
            # Check if column is full
            if board[0][col_index] != " ":
                print("This column is full. Please choose another column.")
                continue
            
            return col_index
        except Exception:
            print("Invalid input. Please try again.")


def place_checker(board, col, checker, rows):
    """Place checker in the specified column."""
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def check_win(board, row, col, checker, rows, cols):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]
    
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


def is_board_full(board, rows, cols):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    """Main game loop."""
    # Initialize board
    board = create_board(ROWS, COLUMNS)
    
    # Get player checkers
    player_checkers = CHECKERS[:PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Game loop
    while True:
        current_player = player_checkers[current_player_index]
        
        # Get valid input from player
        col = get_valid_input(board, COLUMNS, current_player)
        
        # Place checker
        row = place_checker(board, col, current_player, ROWS)
        
        # Print board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, row, col, current_player, ROWS, COLUMNS):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
