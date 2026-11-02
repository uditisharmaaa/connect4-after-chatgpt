import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col):^3} ", end="")
    print()
    
    # Print board with separators
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_column(col_letter, board):
    """Check if the column letter is valid and has space available."""
    if len(col_letter) != 1:
        return False
    
    col_index = ord(col_letter.upper()) - 65
    
    # Check if column index is within bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top cell is empty)
    if board[0][col_index] == " ":
        return True
    
    return False


def get_player_move(board, player_checker):
    """Get valid move from player."""
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if is_valid_column(move, board):
            return ord(move.upper()) - 65
        else:
            print("Invalid move. Please enter a valid column letter.")


def place_checker(board, col, player_checker):
    """Place checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return


def check_win(board, row, col, player_checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_checker)
        
        # Place checker
        place_checker(board, col, current_checker)
        
        # Print board
        print_board(board)
        
        # Get the row where the checker was placed
        placed_row = -1
        for row in range(ROWS):
            if board[row][col] == current_checker:
                placed_row = row
                break
        
        # Check for win
        if check_win(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
