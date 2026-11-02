import os
import random

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers (first NUM_PLAYERS checkers will be used)
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board():
    """Initialize the game board with empty spaces."""
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """Print the current game board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    if len(col_letter) != 1:
        return False
    
    if not col_letter.isalpha():
        return False
    
    col_index = ord(col_letter.upper()) - 65
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False
    
    return True


def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        col_letter = input("Please enter a column (A-" + chr(65 + COLS - 1) + "): ").strip().upper()
        
        if len(col_letter) == 0:
            print("Invalid input. Please try again.")
            continue
        
        if is_valid_column(col_letter, board):
            return ord(col_letter) - 65
        else:
            print("Invalid input. Please try again.")


def place_checker(board, col_index, checker):
    """Place a checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    
    # Check horizontal
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Check top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    # Check bottom-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Check bottom-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        player_number = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column:")
        
        col_index = get_valid_column()
        row_index = place_checker(board, col_index, current_checker)
        
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    board = initialize_board()
    play_game()
