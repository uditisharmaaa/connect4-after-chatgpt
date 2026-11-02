import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board with all cells as spaces."""
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
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if placing a checker in the given column is valid."""
    # Check if column is within bounds
    if col < 0 or col >= COLS:
        return False
    
    # Check if column is not completely filled
    if board[0][col] != " ":
        return False
    
    return True


def get_player_move(board, current_player):
    """Get valid input from the current player and return the column index."""
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("That column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the given column and return the row where it was placed."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
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
    while r < ROWS and board[r][col] == checker:
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
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Get checkers for players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    winner = None
    
    while not game_over:
        # Get current player
        current_player = player_checkers[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_player)
        
        # Place checker on board
        row = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            winner = current_player
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Main program
if __name__ == "__main__":
    play_game()
