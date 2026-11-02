import os
import random

# Constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board with all cells initialized to whitespace."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]


def print_board(board):
    """Print the Connect 4 board with column labels and formatted grid."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_COLS):
        print(f"{chr(ord('A') + col):^3}", end=" ")
    print()
    
    # Print rows
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLS + "+")
        print("|", end="")
        for col in range(BOARD_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * BOARD_COLS + "+")


def get_column_index(col_letter):
    """Convert column letter (A-Z) to column index (0-25). Return -1 if invalid."""
    if len(col_letter) != 1:
        return -1
    col_index = ord(col_letter.upper()) - ord('A')
    if 0 <= col_index < BOARD_COLS:
        return col_index
    return -1


def is_column_full(board, col_index):
    """Check if a column is completely filled with checkers."""
    return board[0][col_index] != " "


def get_placement_row(board, col_index):
    """
    Find the lowest empty row in the given column.
    Return the row index, or -1 if the column is full.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Return True if successful, False if the column is full.
    """
    row = get_placement_row(board, col_index)
    if row == -1:
        return False
    board[row][col_index] = checker
    return True


def check_winner(board, row, col, checker):
    """
    Check if the current placement at (row, col) forms a winning line.
    Return True if 4 or more checkers are in a line, False otherwise.
    """
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the placed checker itself
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        # If 4 or more checkers in a line, it's a win
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_input(player_checker):
    """
    Prompt the player for a column input and validate it.
    Keep asking until a valid input is provided.
    Return the valid column index.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col_index = get_column_index(user_input)
        if col_index == -1:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + BOARD_COLS - 1)}.")
            continue
        
        return col_index


def play_game():
    """Main game loop for Connect 4."""
    board = initialize_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        
        # Get valid column input from player
        while True:
            col_index = get_player_input(current_checker)
            
            # Check if column is full
            if is_column_full(board, col_index):
                print("This column is full. Please choose another column.")
                continue
            
            # Place the checker
            row = get_placement_row(board, col_index)
            place_checker(board, col_index, current_checker)
            break
        
        print_board(board)
        
        # Check for win
        if check_winner(board, row, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
