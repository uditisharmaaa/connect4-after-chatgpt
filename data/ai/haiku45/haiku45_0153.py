import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Possible checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLS):
            board_row.append(" ")
        board.append(board_row)
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_column(column_letter, board):
    """Check if the column letter is valid and not full."""
    # Check if input is a single uppercase letter
    if len(column_letter) != 1 or not column_letter.isupper():
        return False
    
    # Check if letter is within valid range
    col_index = ord(column_letter) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True


def get_valid_column(board):
    """Get a valid column input from the user."""
    while True:
        column_letter = input("Please enter a column: ").upper()
        if is_valid_column(column_letter, board):
            return ord(column_letter) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter.")


def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win at the given position."""
    count = 0
    
    # Check left
    check_col = col - 1
    while check_col >= 0 and board[row][check_col] == checker:
        count += 1
        check_col -= 1
    
    # Check right
    check_col = col + 1
    while check_col < COLS and board[row][check_col] == checker:
        count += 1
        check_col += 1
    
    # Add the current checker
    count += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win at the given position."""
    count = 0
    
    # Check down
    check_row = row + 1
    while check_row < ROWS and board[check_row][col] == checker:
        count += 1
        check_row += 1
    
    # Check up
    check_row = row - 1
    while check_row >= 0 and board[check_row][col] == checker:
        count += 1
        check_row -= 1
    
    # Add the current checker
    count += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker):
    """Check if there is a diagonal win (both directions) at the given position."""
    # Check diagonal from top-left to bottom-right
    count = 0
    check_row = row - 1
    check_col = col - 1
    while check_row >= 0 and check_col >= 0 and board[check_row][check_col] == checker:
        count += 1
        check_row -= 1
        check_col -= 1
    
    check_row = row + 1
    check_col = col + 1
    while check_row < ROWS and check_col < COLS and board[check_row][check_col] == checker:
        count += 1
        check_row += 1
        check_col += 1
    
    count += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 0
    check_row = row - 1
    check_col = col + 1
    while check_row >= 0 and check_col < COLS and board[check_row][check_col] == checker:
        count += 1
        check_row -= 1
        check_col += 1
    
    check_row = row + 1
    check_col = col - 1
    while check_row < ROWS and check_col >= 0 and board[check_row][check_col] == checker:
        count += 1
        check_row += 1
        check_col -= 1
    
    count += 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win(board, row, col, checker):
        return True
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def main():
    """Main game loop."""
    board = initialize_board()
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Starting player: Player {CHECKERS[current_player]}")
    
    game_over = False
    
    while not game_over:
        # Get input from current player
        print(f"Player {CHECKERS[current_player]}, please enter a column: ", end="")
        col = get_valid_column(board)
        
        # Place the checker
        row = place_checker(board, col, CHECKERS[current_player])
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
