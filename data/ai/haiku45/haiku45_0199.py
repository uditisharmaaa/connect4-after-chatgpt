import os
import random

# Global constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print board with separators
    for row in range(rows):
        # Print separator line
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+---" * cols + "+")


def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    cols = len(board[0])
    
    # Check if column index is within bounds
    if col < 0 or col >= cols:
        return False
    
    # Check if column is not full
    if board[0][col] != " ":
        return False
    
    return True


def get_player_input(board, player_checker):
    """Get valid input from player for column choice."""
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input format
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is valid
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1  # Should not reach here if is_valid_move is called first


def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win at the given position."""
    cols = len(board[0])
    count = 1
    
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win at the given position."""
    rows = len(board)
    count = 1
    
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_slash(board, row, col, checker):
    """Check if there is a diagonal win (/) at the given position."""
    rows = len(board)
    cols = len(board[0])
    count = 1
    
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_backslash(board, row, col, checker):
    """Check if there is a diagonal win (\\) at the given position."""
    rows = len(board)
    cols = len(board[0])
    count = 1
    
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the placed checker results in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win_slash(board, row, col, checker):
        return True
    if check_diagonal_win_backslash(board, row, col, checker):
        return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Get player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid move from player
        col = get_player_input(board, current_player)
        
        # Place checker
        row = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
