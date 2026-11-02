import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """Initialize the board with empty spaces."""
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    rows = len(board)
    columns = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(f"{chr(65 + col):^3} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for _ in range(columns):
            print("---+", end="")
        print()
        
        # Cell content
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for _ in range(columns):
        print("---+", end="")
    print()


def get_valid_input(num_players, checkers, current_player, columns):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {checkers[current_player]}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within board bounds
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input. Please enter a column between A and {chr(65 + columns - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, current_player, checkers):
    """Place a checker in the specified column. Returns True if successful."""
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checkers[current_player]
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, row, col, current_player, checkers):
    """Check if the current player has won after placing a checker at (row, col)."""
    player_checker = checkers[current_player]
    rows = len(board)
    columns = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == player_checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < columns and board[row][c] == player_checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == player_checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == player_checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == player_checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < columns and board[r][c] == player_checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < columns and board[r][c] == player_checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == player_checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def get_row_after_placement(board, col):
    """Get the row where the last checker was placed in the given column."""
    for row in range(len(board)):
        if board[row][col] != " ":
            return row
    return len(board) - 1


def check_draw(board):
    """Check if the board is completely filled (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game(rows, columns, num_players):
    """Main game loop."""
    checkers = CHECKERS[:num_players]
    board = initialize_board(rows, columns)
    
    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)
    
    print_board(board)
    
    while True:
        # Get valid input from player
        while True:
            col = get_valid_input(num_players, checkers, current_player, columns)
            if place_checker(board, col, current_player, checkers):
                # Find the row where the checker was placed
                row = get_row_after_placement(board, col)
                break
        
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player, checkers):
            print(f"Player {checkers[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % num_players


def main():
    """Entry point of the program."""
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
