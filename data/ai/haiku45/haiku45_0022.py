import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    board = []
    for row in range(rows):
        board.append([" " for col in range(cols)])
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+---", end="")
        for col in range(cols - 1):
            print("+---", end="")
        print("+")
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Bottom border
    print("+---", end="")
    for col in range(cols - 1):
        print("+---", end="")
    print("+")


def is_valid_column(column_input, cols):
    """Validate if the column input is valid."""
    if len(column_input) != 1:
        return False
    
    if not column_input.isalpha():
        return False
    
    column_letter = column_input.upper()
    column_index = ord(column_letter) - ord('A')
    
    if column_index < 0 or column_index >= cols:
        return False
    
    return True


def get_column_index(column_input):
    """Convert column letter to column index."""
    return ord(column_input.upper()) - ord('A')


def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1  # Column is full


def check_horizontal_win(board, row, col, checker):
    """Check if there's a horizontal win at the given position."""
    cols = len(board[0])
    count = 0
    
    # Count consecutive checkers to the left
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count consecutive checkers to the right
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there's a vertical win at the given position."""
    rows = len(board)
    count = 0
    
    # Count consecutive checkers above
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count consecutive checkers below
    for r in range(row + 1, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_ascending(board, row, col, checker):
    """Check diagonal win (bottom-left to top-right direction)."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    
    # Count consecutive checkers down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c -= 1
    
    # Count the current checker
    count += 1
    
    # Count consecutive checkers up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_descending(board, row, col, checker):
    """Check diagonal win (top-left to bottom-right direction)."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    
    # Count consecutive checkers up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c -= 1
    
    # Count the current checker
    count += 1
    
    # Count consecutive checkers down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win_ascending(board, row, col, checker):
        return True
    if check_diagonal_win_descending(board, row, col, checker):
        return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        current_player_name = chr(65 + current_player_index) if current_player_index > 1 else current_checker
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            
            if not is_valid_column(user_input, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = get_column_index(user_input)
            
            if is_column_full(board, col_index):
                print("This column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
