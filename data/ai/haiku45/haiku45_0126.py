import os
import random

# Constants for board configuration
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create a board with the specified dimensions, initialized with spaces."""
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            board_row.append(" ")
        board.append(board_row)
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_column_from_input(user_input, cols):
    """
    Convert user input to column index.
    Returns column index if valid, otherwise returns -1.
    """
    # Check if input is a single uppercase letter
    if len(user_input) != 1 or not user_input.isupper() or not user_input.isalpha():
        return -1
    
    # Convert letter to column index
    col = ord(user_input) - ord('A')
    
    # Check if column is within bounds
    if col < 0 or col >= cols:
        return -1
    
    return col


def is_column_full(board, col):
    """Check if a column is completely filled."""
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, rows, cols, checker):
    """Check if there is a horizontal win for the given checker."""
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    return False


def check_vertical_win(board, rows, cols, checker):
    """Check if there is a vertical win for the given checker."""
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    return False


def check_diagonal_down_right_win(board, rows, cols, checker):
    """Check if there is a diagonal win (top-left to bottom-right) for the given checker."""
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    return False


def check_diagonal_down_left_win(board, rows, cols, checker):
    """Check if there is a diagonal win (top-right to bottom-left) for the given checker."""
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if (board[row][col] == checker and
                board[row + 1][col - 1] == checker and
                board[row + 2][col - 2] == checker and
                board[row + 3][col - 3] == checker):
                return True
    return False


def check_win(board, checker):
    """Check if the given checker has won the game."""
    rows = len(board)
    cols = len(board[0])
    
    if check_horizontal_win(board, rows, cols, checker):
        return True
    if check_vertical_win(board, rows, cols, checker):
        return True
    if check_diagonal_down_right_win(board, rows, cols, checker):
        return True
    if check_diagonal_down_left_win(board, rows, cols, checker):
        return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    cols = len(board[0])
    for col in range(cols):
        if not is_column_full(board, col):
            return False
    return True


def play_game():
    """Main game loop."""
    # Create and display initial board
    board = create_board(BOARD_ROWS, BOARD_COLS)
    print_board(board)
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    game_over = False
    
    while not game_over:
        # Prompt current player for input
        player_number = current_player_index + 1
        print(f"Player {current_checker}, please enter a column: ", end="")
        user_input = input().strip().upper()
        
        # Validate input
        col = get_column_from_input(user_input, BOARD_COLS)
        
        if col == -1:
            print("Invalid input. Please enter a column letter (A-" + chr(ord('A') + BOARD_COLS - 1) + ").")
            continue
        
        # Check if column is full
        if is_column_full(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        # Place checker
        place_checker(board, col, current_checker)
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            game_over = True
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]


if __name__ == "__main__":
    play_game()
