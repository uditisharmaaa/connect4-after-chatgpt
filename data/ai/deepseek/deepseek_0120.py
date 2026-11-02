import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    # Print column labels
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print("+" + "---+" * COLS)
    
    for row in board:
        # Print row content
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        # Print row border
        print("+" + "---+" * COLS)

def is_valid_input(col, board):
    """Check if the player's input is valid."""
    if len(col) != 1 or not col.isupper() or not col.isalpha():
        return False
    col_idx = ord(col) - ord('A')
    return 0 <= col_idx < COLS and board[0][col_idx] == " "

def get_player_move(player, board):
    """Get and validate player's move."""
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if is_valid_input(move, board):
            return ord(move) - ord('A')
        print("Invalid input. Please try again.")

def place_checker(board, col_idx, player):
    """Place the player's checker in the specified column."""
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player
            return row_idx
    return -1  # Column is full (shouldn't happen if input is validated)

def check_win(board, row, col, player):
    """Check if the current move results in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != " " for cell in board[0])

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    os.system('clear')
    print_board(board)
    
    while True:
        col_idx = get_player_move(current_player, board)
        row_idx = place_checker(board, col_idx, current_player)
        os.system('clear')
        print_board(board)
        
        if check_win(board, row_idx, col_idx, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
