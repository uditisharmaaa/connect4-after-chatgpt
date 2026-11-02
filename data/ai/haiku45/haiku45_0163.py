import os
import random

# Constants
COLUMNS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """Create and return a board with all cells initialized to spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def get_column_letter(col_index):
    """Convert column index to letter (0 -> A, 1 -> B, etc.)."""
    return chr(ord("A") + col_index)


def print_board(board, cols):
    """Print the current state of the board."""
    os.system("clear")
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {get_column_letter(col)}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column_input(col_letter, cols):
    """Check if the column input is valid."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_index = ord(col_letter.upper()) - ord("A")
    return 0 <= col_index < cols


def get_column_index(col_letter):
    """Convert column letter to index."""
    return ord(col_letter.upper()) - ord("A")


def can_place_checker(board, col_index, rows):
    """Check if a checker can be placed in the given column."""
    return board[0][col_index] == " "


def place_checker(board, col_index, checker, rows):
    """Place a checker in the given column and return the row index."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_horizontal_win(board, row, col, checker, cols):
    """Check if there's a horizontal win at the given position."""
    count = 1
    
    # Check left
    col_check = col - 1
    while col_check >= 0 and board[row][col_check] == checker:
        count += 1
        col_check -= 1
    
    # Check right
    col_check = col + 1
    while col_check < cols and board[row][col_check] == checker:
        count += 1
        col_check += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker, rows):
    """Check if there's a vertical win at the given position."""
    count = 1
    
    # Check down
    row_check = row + 1
    while row_check < rows and board[row_check][col] == checker:
        count += 1
        row_check += 1
    
    # Check up
    row_check = row - 1
    while row_check >= 0 and board[row_check][col] == checker:
        count += 1
        row_check -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker, rows, cols):
    """Check if there's a diagonal win at the given position (both diagonals)."""
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Check up-left
    row_check, col_check = row - 1, col - 1
    while row_check >= 0 and col_check >= 0 and board[row_check][col_check] == checker:
        count += 1
        row_check -= 1
        col_check -= 1
    
    # Check down-right
    row_check, col_check = row + 1, col + 1
    while row_check < rows and col_check < cols and board[row_check][col_check] == checker:
        count += 1
        row_check += 1
        col_check += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check up-right
    row_check, col_check = row - 1, col + 1
    while row_check >= 0 and col_check < cols and board[row_check][col_check] == checker:
        count += 1
        row_check -= 1
        col_check += 1
    
    # Check down-left
    row_check, col_check = row + 1, col - 1
    while row_check < rows and col_check >= 0 and board[row_check][col_check] == checker:
        count += 1
        row_check += 1
        col_check -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker, rows, cols):
    """Check if the last move resulted in a win."""
    if check_horizontal_win(board, row, col, checker, cols):
        return True
    if check_vertical_win(board, row, col, checker, rows):
        return True
    if check_diagonal_win(board, row, col, checker, rows, cols):
        return True
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def get_valid_column_input(cols):
    """Get and validate column input from the player."""
    while True:
        user_input = input("Enter a column (A-" + get_column_letter(cols - 1) + "): ").strip()
        
        if not is_valid_column_input(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(user_input)
        return col_index


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLUMNS)
    checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board, COLUMNS)
    print(f"Game started! Player {checkers[current_player_index]} goes first.")
    input("Press Enter to continue...")
    
    while True:
        print_board(board, COLUMNS)
        current_checker = checkers[current_player_index]
        
        # Get valid column input
        while True:
            col_index = get_valid_column_input(COLUMNS)
            
            if not can_place_checker(board, col_index, ROWS):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker and get the row where it was placed
        row_index = place_checker(board, col_index, current_checker, ROWS)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker, ROWS, COLUMNS):
            print_board(board, COLUMNS)
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLUMNS):
            print_board(board, COLUMNS)
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    play_game()
