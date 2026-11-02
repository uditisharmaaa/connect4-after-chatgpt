import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    board = []
    for row in range(BOARD_HEIGHT):
        board.append([" " for col in range(BOARD_WIDTH)])
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(BOARD_WIDTH):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with borders
    for row in range(BOARD_HEIGHT):
        # Print top border
        print("+---" * BOARD_WIDTH + "+")
        
        # Print row content
        print("|", end="")
        for col in range(BOARD_WIDTH):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * BOARD_WIDTH + "+")


def get_valid_column(current_player_checker):
    """Get a valid column input from the player."""
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if user_input not in [chr(65 + i) for i in range(BOARD_WIDTH)]:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + BOARD_WIDTH - 1)}.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is not full
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the last placed checker at (row, col) resulted in a win."""
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < BOARD_WIDTH and board[row][c] == checker:
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
    while r < BOARD_HEIGHT and board[r][col] == checker:
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
    while r < BOARD_HEIGHT and c < BOARD_WIDTH and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < BOARD_WIDTH and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < BOARD_HEIGHT and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    global board
    
    # Initialize the board
    board = initialize_board()
    
    # Get players' checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player_checker = players[current_player_index]
        
        # Get valid column from player
        col = get_valid_column(current_player_checker)
        
        # Place checker on the board
        row = place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Main execution
if __name__ == "__main__":
    board = None
    play_game()
