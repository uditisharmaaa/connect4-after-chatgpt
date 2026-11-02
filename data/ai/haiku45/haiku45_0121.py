import os
import random

# Constants
NUM_COLS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and initialize the board with empty spaces."""
    board = []
    for row in range(NUM_ROWS):
        board.append([" " for col in range(NUM_COLS)])
    return board

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(NUM_COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+---" * NUM_COLS + "+")
    
    # Print each row
    for row in range(NUM_ROWS):
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * NUM_COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    if col < 0 or col >= NUM_COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def get_player_move(board, player_num):
    """Get and validate the player's move."""
    checker = CHECKERS[player_num]
    while True:
        move = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column number
        col = ord(move) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= NUM_COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + NUM_COLS - 1)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal right
        (1, -1)   # diagonal left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        # Get the current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid move from player
        col = get_player_move(board, current_player)
        
        # Place the checker and find which row it was placed in
        for row in range(NUM_ROWS - 1, -1, -1):
            if board[row][col] == " ":
                board[row][col] = checker
                break
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("Draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
