import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return a board with all cells initialized to spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board


def print_board(board):
    """Print the Connect 4 board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), "  ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()


def get_valid_column(player_checker):
    """Get valid column input from player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col_index, player_checker):
    """Place checker in the lowest available position in the column."""
    # Find the lowest empty row in the column (start from bottom)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, player_checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def get_next_player(current_player_index):
    """Return the index of the next player."""
    return (current_player_index + 1) % NUM_PLAYERS


def play_game():
    """Main game loop."""
    board = initialize_board()
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid column from player
        col_index = get_valid_column(current_player_checker)
        
        # Try to place checker
        if place_checker(board, col_index, current_player_checker):
            print_board(board)
            
            # Check for win
            if check_win(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                break
            
            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                break
            
            # Move to next player
            current_player_index = get_next_player(current_player_index)
        else:
            # Invalid move (column full), print board and ask again
            print_board(board)


def main():
    """Start the Connect 4 game."""
    play_game()


if __name__ == "__main__":
    main()
