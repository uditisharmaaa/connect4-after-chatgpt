import os
import random

# Constants
COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board with all cells initialized to spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print top border
    print(" +", end="")
    for _ in range(COLS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print(" |", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print border after each row
        print(" +", end="")
        for _ in range(COLS):
            print("---+", end="")
        print()


def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True


def get_player_input(board, player_checker):
    """Get and validate player input."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter, not a number or special character.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is in valid range
        if col < 0 or col >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
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


def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Choose random starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    # Game loop
    while True:
        player_checker = CHECKERS[current_player]
        
        # Get player input
        col = get_player_input(board, player_checker)
        
        # Place checker
        row = place_checker(board, col, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % PLAYERS


if __name__ == "__main__":
    play_game()
