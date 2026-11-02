import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Create and return a board with the specified dimensions.
    All cells are initialized with empty spaces.
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the board in a formatted manner with column labels and borders.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    rows = len(board)
    for row in range(rows):
        # Top border
        print("+---" * cols + "+")
        
        # Cell content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+---" * cols + "+")


def is_valid_input(column_letter, cols):
    """
    Validate user input. Check if it's a single letter and within board bounds.
    Returns the column index if valid, or -1 if invalid.
    """
    if len(column_letter) != 1:
        return -1
    
    if not column_letter.isalpha():
        return -1
    
    column_index = ord(column_letter.upper()) - ord('A')
    
    if column_index < 0 or column_index >= cols:
        return -1
    
    return column_index


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    Returns True if there's at least one empty cell, False otherwise.
    """
    return board[0][col] == ' '


def place_checker(board, col, checker):
    """
    Place a checker in the specified column. It falls to the lowest available position.
    Returns the row where the checker was placed.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    
    return -1  # Column is full


def check_horizontal_win(board, row, col, checker, cols):
    """
    Check if there's a horizontal win at the current position.
    """
    count = 0
    
    # Count checkers to the left
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count checkers to the right
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker, rows):
    """
    Check if there's a vertical win at the current position.
    """
    count = 0
    
    # Count checkers above
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count checkers below
    for r in range(row + 1, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_left_right(board, row, col, checker, rows, cols):
    """
    Check if there's a diagonal win (top-left to bottom-right) at the current position.
    """
    count = 0
    
    # Count checkers in top-left direction
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count checkers in bottom-right direction
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_right_left(board, row, col, checker, rows, cols):
    """
    Check if there's a diagonal win (top-right to bottom-left) at the current position.
    """
    count = 0
    
    # Count checkers in top-right direction
    r, c = row - 1, col + 1
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    
    # Count the current checker
    count += 1
    
    # Count checkers in bottom-left direction
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """
    Check if the current move results in a win.
    """
    rows = len(board)
    cols = len(board[0])
    
    if check_horizontal_win(board, row, col, checker, cols):
        return True
    
    if check_vertical_win(board, row, col, checker, rows):
        return True
    
    if check_diagonal_win_left_right(board, row, col, checker, rows, cols):
        return True
    
    if check_diagonal_win_right_left(board, row, col, checker, rows, cols):
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def get_player_input(player_checker, cols):
    """
    Get and validate player input for column selection.
    Keeps asking until valid input is received.
    """
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            
            col_index = is_valid_input(user_input, cols)
            
            if col_index == -1:
                print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(ord('A') + cols - 1)))
                continue
            
            return col_index
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            exit()
        except Exception as e:
            print("Invalid input. Please try again.")


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    game_over = False
    winner = None
    
    # Game loop
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        # Get valid input from player
        col = get_player_input(current_checker, COLS)
        
        # Check if column is full
        if not can_place_checker(board, col):
            print(f"Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        row = place_checker(board, col, current_checker)
        
        # Print board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            winner = current_checker
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
