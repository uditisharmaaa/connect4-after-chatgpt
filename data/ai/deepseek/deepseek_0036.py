import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows with borders
    for row in board:
        print("+" + "---+" * COLS)
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    # Print the bottom border
    print("+" + "---+" * COLS)

def get_valid_move(board, player):
    """Prompt the player for a valid move and return the column index."""
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column out of range. Please choose between A-{chr(65 + COLS - 1)}.")
            continue
        
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column at the lowest empty row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return row
    return -1  # Column is full

def check_win(board, row, col, player):
    """Check if the current move results in a win."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # current cell counts as 1
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    while True:
        current_player = PLAYER_SYMBOLS[current_player_idx]
        print_board(board)
        
        col = get_valid_move(board, current_player)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
