import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_CHARS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

def initialize_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print the top border
    print("+" + "---+" * COLS)
    
    for row in board:
        # Print each cell in the row with borders
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "---+" * COLS)

def get_player_input(player_char):
    """Prompt the player for a column and return the validated column index."""
    while True:
        try:
            col = input(f"Player {player_char}, please enter a column: ").upper()
            if len(col) != 1 or not col.isalpha():
                print("Invalid input. Please enter a single letter (A-G).")
                continue
            col_idx = ord(col) - ord('A')
            if col_idx < 0 or col_idx >= COLS:
                print(f"Column out of range. Please enter a letter between A-{chr(65 + COLS - 1)}.")
                continue
            return col_idx
        except EOFError:
            print("Invalid input. Please try again.")

def place_checker(board, col_idx, player_char):
    """Place the player's checker in the specified column if possible.
    Return True if placement was successful, False otherwise (column full)."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_char
            return True
    return False

def check_win(board, player_char):
    """Check if the current player has won by connecting 4 checkers.
    Returns True if a win condition is met, False otherwise."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player_char:
                for dr, dc in directions:
                    count = 1
                    for step in range(1, 4):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_char:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return True
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if " " in row:
            return False
    return True

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    player_chars = PLAYER_CHARS[:NUM_PLAYERS]
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join([f'Player {c}' for c in player_chars])}")
    print(f"Player {player_chars[current_player]} starts first.")
    print_board(board)
    
    while True:
        player_char = player_chars[current_player]
        col_idx = get_player_input(player_char)
        
        if not place_checker(board, col_idx, player_char):
            print("Column is full. Player loses turn.")
        else:
            print_board(board)
            if check_win(board, player_char):
                print(f"Player {player_char} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
