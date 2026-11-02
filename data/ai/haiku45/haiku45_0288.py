import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create an empty board with the specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border of row
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    cols = len(board[0])
    
    if col < 0 or col >= cols:
        return False
    
    # Check if the top row of the column is empty
    if board[0][col] != " ":
        return False
    
    return True

def get_player_move(board, player_checker):
    """Get a valid move from the player."""
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if user_input < 'A' or user_input >= chr(65 + cols):
            print(f"Invalid column. Please enter a letter from A to {chr(64 + cols)}.")
            continue
        
        col = ord(user_input) - 65
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1  # Should not happen if is_valid_move is called first

def check_winner(board, row, col, checker):
    """Check if the last move resulted in a win."""
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (two directions)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
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
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_next_player(current_player, num_players):
    """Get the next player index."""
    return (current_player + 1) % num_players

def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {checkers[current_player]} will start!")
    print()
    
    game_over = False
    
    while not game_over:
        # Get player move
        col = get_player_move(board, checkers[current_player])
        
        # Place checker
        row = place_checker(board, col, checkers[current_player])
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_winner(board, row, col, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = get_next_player(current_player, NUM_PLAYERS)
            print()

if __name__ == "__main__":
    play_game()
