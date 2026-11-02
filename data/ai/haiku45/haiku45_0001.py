import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return a board with all empty cells."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLUMNS)])
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLUMNS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
        print("+", end="")
        for col in range(COLUMNS):
            print("---+", end="")
        print()


def is_valid_column(column_letter, board):
    """Check if column letter is valid and not full."""
    # Check if it's a single letter
    if len(column_letter) != 1:
        return False
    
    # Check if it's uppercase
    if not column_letter.isupper():
        return False
    
    # Check if it's a valid column
    col_index = ord(column_letter) - ord('A')
    if col_index < 0 or col_index >= COLUMNS:
        return False
    
    # Check if column is full
    if board[0][col_index] != " ":
        return False
    
    return True


def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter) - ord('A')


def place_checker(board, column_index, checker):
    """Place checker in the lowest available position in column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True
    return False


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
    while c < COLUMNS and board[row][c] == checker:
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
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLUMNS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def find_row_for_column(board, col_index):
    """Find the row where the checker will be placed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    winner = None
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        player_name = current_player_index + 1
        
        # Get valid input from player
        while True:
            column_letter = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            if is_valid_column(column_letter, board):
                break
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place the checker
        col_index = get_column_index(column_letter)
        row_index = find_row_for_column(board, col_index)
        place_checker(board, col_index, current_checker)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            winner = current_checker
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
