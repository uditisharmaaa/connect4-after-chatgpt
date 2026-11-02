import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column labels
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    
    # Print top border
    print("+" + "---+" * NUM_COLS)
    
    # Print each row
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "---+" * NUM_COLS)

def get_valid_column_input(current_player):
    """Get and validate the column input from the current player."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1:
            print("Invalid input! Please enter a single letter.")
            continue
        col_idx = ord(column) - ord('A')
        if col_idx < 0 or col_idx >= NUM_COLS:
            print(f"Invalid column! Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
            continue
        return col_idx

def place_checker(board, col_idx, current_player):
    """Place the checker in the specified column if possible."""
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = current_player
            return True
    return False

def check_win(board, row, col, current_player):
    """Check if the current move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(max(0, col - 3), min(NUM_COLS, col + 4)):
        if board[row][c] == current_player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(max(0, row - 3), min(NUM_ROWS, row + 4)):
        if board[r][col] == current_player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    for i in range(-3, 4):
        r, c = row + i, col + i
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            if board[r][c] == current_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    for i in range(-3, 4):
        r, c = row + i, col - i
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            if board[r][c] == current_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if " " in row:
            return False
    return True

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        col_idx = get_valid_column_input(current_player)
        
        if not place_checker(board, col_idx, current_player):
            print("Column is full! You lose your turn.")
            continue
        
        # Find the row where the checker was placed
        for row_idx in range(NUM_ROWS):
            if board[row_idx][col_idx] == current_player:
                break
        
        if check_win(board, row_idx, col_idx, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch players
        current_player_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_player_index + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
