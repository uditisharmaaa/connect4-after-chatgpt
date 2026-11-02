import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board rows
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")


def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True


def place_checker(board, col_letter, checker):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    
    return None, None


def check_win(board, row, col, checker):
    """Check if the current player has won."""
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, checker, -1, 1):
        return True
    
    return False


def check_direction(board, row, col, checker, row_dir, col_dir):
    """Check if there are 4 checkers in a row in a given direction."""
    count = 1
    
    # Check in positive direction
    r, c = row + row_dir, col + col_dir
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        count += 1
        r += row_dir
        c += col_dir
    
    # Check in negative direction
    r, c = row - row_dir, col - col_dir
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        count += 1
        r -= row_dir
        c -= col_dir
    
    return count >= WIN_LENGTH


def is_board_full(board):
    """Check if the board is completely filled."""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column: ", end="")
        
        col_input = input().strip()
        
        # Validate input
        if not is_valid_column(col_input, board):
            print_board(board)
            print("Invalid input. Please try again.")
            continue
        
        # Place the checker
        row, col = place_checker(board, col_input, current_checker)
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
