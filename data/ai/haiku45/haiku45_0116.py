import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * cols + "+")


def is_valid_input(column_letter, cols):
    """Check if the input is a valid column letter."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    col_index = ord(column_letter.upper()) - ord('A')
    return 0 <= col_index < cols


def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, col, rows):
    """Check if a checker can be placed in the given column."""
    return board[0][col] == " "


def place_checker(board, col, checker, rows):
    """Place a checker in the given column and return the row where it was placed."""
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full


def check_horizontal_win(board, row, col, checker, rows, cols):
    """Check if there's a horizontal win at the placed checker position."""
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker, rows, cols):
    """Check if there's a vertical win at the placed checker position."""
    count = 1
    
    # Check down
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker, rows, cols):
    """Check if there's a diagonal win (both directions) at the placed checker position."""
    # Check diagonal from top-left to bottom-right
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker, rows, cols):
    """Check if the placed checker results in a win."""
    if check_horizontal_win(board, row, col, checker, rows, cols):
        return True
    if check_vertical_win(board, row, col, checker, rows, cols):
        return True
    if check_diagonal_win(board, row, col, checker, rows, cols):
        return True
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full (draw condition)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def get_player_move(board, current_player, checker, rows, cols):
    """Get a valid move from the current player."""
    while True:
        column_input = input(f"Player {checker}, please enter a column: ").strip()
        
        # Validate input
        if not is_valid_input(column_input, cols):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(ord('A') + cols - 1)))
            continue
        
        col = get_column_index(column_input)
        
        # Check if column is full
        if not can_place_checker(board, col, rows):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game(rows, cols, num_players):
    """Main game loop."""
    # Initialize board
    board = initialize_board(rows, cols)
    
    # Get checkers for this game
    game_checkers = CHECKERS[:num_players]
    
    # Randomly select first player
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    
    game_over = False
    winner = None
    
    # Main game loop
    while not game_over:
        checker = game_checkers[current_player]
        
        # Get player move
        col = get_player_move(board, current_player, checker, rows, cols)
        
        # Place checker
        row = place_checker(board, col, checker, rows)
        
        # Print board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row, col, checker, rows, cols):
            print(f"Player {checker} won!")
            game_over = True
            winner = checker
        
        # Check for draw
        elif is_board_full(board, rows, cols):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player = (current_player + 1) % num_players


def main():
    """Main function to start the game."""
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
