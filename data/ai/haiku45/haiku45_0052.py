import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """Print the current state of the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(col_input, cols):
    """Validate if the column input is valid and within board bounds."""
    if len(col_input) != 1:
        return False
    
    if not col_input.isalpha():
        return False
    
    col_input = col_input.upper()
    col_index = ord(col_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_index(col_input):
    """Convert column letter to index (0-based)."""
    return ord(col_input.upper()) - ord('A')


def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available position."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker, cols, rows):
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
    while c < cols and board[row][c] == checker:
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
    while r < rows and board[r][col] == checker:
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
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board, cols):
    """Check if the board is completely full (draw condition)."""
    for col in range(cols):
        if not is_column_full(board, col):
            return False
    return True


def get_valid_move(num_players, current_player, board, cols):
    """Get a valid column input from the current player."""
    checker = CHECKERS[current_player]
    
    while True:
        col_input = input(f"Player {checker}, please enter a column: ")
        
        if not is_valid_column(col_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(col_input)
        
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game(rows, cols, num_players):
    """Main game loop."""
    board = create_board(rows, cols)
    current_player = random.randint(0, num_players - 1)
    
    print_board(board, cols)
    
    while True:
        # Get valid move from current player
        col_index = get_valid_move(num_players, current_player, board, cols)
        
        # Place checker
        checker = CHECKERS[current_player]
        row = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row, col_index, checker, cols, rows):
            print(f"Player {checker} won!")
            return
        
        # Check for draw
        if is_board_full(board, cols):
            print("It's a draw!")
            return
        
        # Move to next player
        current_player = (current_player + 1) % num_players


def main():
    """Entry point of the program."""
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
