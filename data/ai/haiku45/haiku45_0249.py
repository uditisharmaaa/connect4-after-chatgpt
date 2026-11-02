import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return a board with all empty spaces."""
    board = []
    for row in range(ROWS):
        new_row = []
        for col in range(COLS):
            new_row.append(" ")
        board.append(new_row)
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def is_valid_column(column_input):
    """Check if the column input is valid."""
    if len(column_input) != 1:
        return False
    
    if not column_input.isalpha():
        return False
    
    column_index = ord(column_input.upper()) - 65
    
    if column_index < 0 or column_index >= COLS:
        return False
    
    return True


def get_column_from_input(column_input):
    """Convert column letter to column index."""
    return ord(column_input.upper()) - 65


def can_place_checker(board, column):
    """Check if a checker can be placed in the column."""
    if board[0][column] == " ":
        return True
    return False


def place_checker(board, column, checker):
    """Place a checker in the specified column and return the row."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row
    return -1


def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win at the given position."""
    count = 0
    
    # Count to the left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Count to the right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    
    # Add the current position
    count += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win at the given position."""
    count = 0
    
    # Count downwards
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    
    # Count upwards
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    # Add the current position
    count += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_right(board, row, col, checker):
    """Check if there is a diagonal win (going down-right and up-left)."""
    count = 0
    
    # Count down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    # Count up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    # Add the current position
    count += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_left(board, row, col, checker):
    """Check if there is a diagonal win (going down-left and up-right)."""
    count = 0
    
    # Count down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    # Count up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Add the current position
    count += 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the player has won."""
    if check_horizontal_win(board, row, col, checker):
        return True
    
    if check_vertical_win(board, row, col, checker):
        return True
    
    if check_diagonal_win_right(board, row, col, checker):
        return True
    
    if check_diagonal_win_left(board, row, col, checker):
        return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def get_player_move(board, player_checker):
    """Get a valid move from the player."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        
        column = get_column_from_input(column_input)
        
        if not can_place_checker(board, column):
            print("This column is full. Please choose another column.")
            continue
        
        return column


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get the player checkers for this game
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = players[current_player_index]
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get player move
        column = get_player_move(board, current_checker)
        
        # Place the checker and get the row
        row = place_checker(board, column, current_checker)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = players[current_player_index]


if __name__ == "__main__":
    play_game()
