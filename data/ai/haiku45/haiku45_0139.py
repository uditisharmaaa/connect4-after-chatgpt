import os
import random

# Configuration constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Available checker symbols for up to 5 players
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col):^3} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def get_valid_column(players, current_player_idx, board):
    """Get a valid column input from the current player."""
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {players[current_player_idx]}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if user_input < 'A' or user_input >= chr(65 + cols):
            print(f"Invalid column. Please enter a letter between A and {chr(64 + cols)}.")
            continue
        
        col_idx = ord(user_input) - 65
        
        # Check if column is full
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_idx


def place_checker(board, col_idx, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    rows = len(board)
    
    # Find the lowest empty space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """Check if the placed checker results in a win."""
    rows = len(board)
    cols = len(board[0])
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal, Anti-diagonal
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
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


def check_draw(board):
    """Check if the board is full (draw condition)."""
    return all(cell != ' ' for cell in board[0])


def get_random_player(num_players):
    """Return a random starting player index."""
    return random.randint(0, num_players - 1)


def play_game():
    """Main game loop."""
    # Initialize game
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    players = CHECKER_SYMBOLS[:NUM_PLAYERS]
    current_player_idx = get_random_player(NUM_PLAYERS)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get valid column from current player
        col_idx = get_valid_column(players, current_player_idx, board)
        
        # Place checker
        row_idx = place_checker(board, col_idx, players[current_player_idx])
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_idx, col_idx, players[current_player_idx]):
            print(f"Player {players[current_player_idx]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
