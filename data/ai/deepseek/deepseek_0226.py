import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Possible player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Initialize an empty game board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    
    # Print the board rows with borders
    border = "+" + ("---+") * len(board[0])
    print(border)
    
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += " {} |".format(cell)
        print(row_str)
        print(border)

def get_valid_column_input(current_player, cols):
    """Get and validate column input from the player."""
    while True:
        try:
            col = input(f"Player {current_player}, please enter a column: ").upper()
            if len(col) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            col_idx = ord(col) - ord('A')
            if col_idx < 0 or col_idx >= cols:
                print(f"Column must be between A and {chr(ord('A') + cols - 1)}.")
                continue
            
            return col_idx
        except Exception:
            print("Invalid input. Please enter a column letter (A, B, C, ...).")

def place_checker(board, col_idx, checker):
    """Place a checker in the specified column at the lowest available row.
    Returns True if placement was successful, False otherwise."""
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current cell
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    clear_screen()
    board = initialize_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    print("Welcome to Connect 4!")
    print("A random player has been chosen to start.")
    print_board(board)
    
    while True:
        col_idx = get_valid_column_input(current_player, COLS)
        
        if not place_checker(board, col_idx, current_player):
            print("Column is full. Try another column.")
            continue
        
        clear_screen()
        print_board(board)
        
        # Find the row where the checker was placed
        placed_row = -1
        for r in range(ROWS):
            if board[r][col_idx] == current_player:
                placed_row = r
                break
        
        if check_win(board, placed_row, col_idx, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
