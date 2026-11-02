import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Initialize the board with empty spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board


def print_board(board):
    """Print the board in a formatted way."""
    os.system("clear")
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * COLS + "+")


def get_column_input(board, current_player):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if the letter is within the valid range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        # Check if the column is not full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """Place a checker in the specified column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return row
    return -1


def check_horizontal_win(board, row, col, player_checker):
    """Check if there's a horizontal win."""
    count = 0
    
    # Check to the left
    c = col
    while c >= 0 and board[row][c] == player_checker:
        count += 1
        c -= 1
    
    # Check to the right (don't count the current cell twice)
    c = col + 1
    while c < COLS and board[row][c] == player_checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, player_checker):
    """Check if there's a vertical win."""
    count = 0
    
    # Check downwards
    r = row
    while r < ROWS and board[r][col] == player_checker:
        count += 1
        r += 1
    
    # Check upwards (don't count the current cell twice)
    r = row - 1
    while r >= 0 and board[r][col] == player_checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, player_checker):
    """Check if there's a diagonal win (both directions)."""
    # Check diagonal from top-left to bottom-right
    count = 0
    r, c = row, col
    
    # Check up-left
    while r >= 0 and c >= 0 and board[r][c] == player_checker:
        count += 1
        r -= 1
        c -= 1
    
    # Check down-right (don't count the current cell twice)
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == player_checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 0
    r, c = row, col
    
    # Check up-right
    while r >= 0 and c < COLS and board[r][c] == player_checker:
        count += 1
        r -= 1
        c += 1
    
    # Check down-left (don't count the current cell twice)
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == player_checker:
        count += 1
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, player_checker):
    """Check if the current move results in a win."""
    if check_horizontal_win(board, row, col, player_checker):
        return True
    if check_vertical_win(board, row, col, player_checker):
        return True
    if check_diagonal_win(board, row, col, player_checker):
        return True
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get player input
        col = get_column_input(board, current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to the next player
        current_player = (current_player + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
