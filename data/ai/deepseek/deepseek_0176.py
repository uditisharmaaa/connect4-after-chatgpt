import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print("+" + "---+" * COLS)
    
    for row in board:
        # Print row content
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        # Print row border
        print("+" + "---+" * COLS)

def is_valid_column(col_input):
    """Check if the column input is valid."""
    if len(col_input) != 1:
        return False
    col = ord(col_input.upper()) - ord('A')
    return 0 <= col < COLS

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def play_game():
    """Play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        checker = PLAYER_CHECKS[current_player]
        print(f"Player {checker}, please enter a column: ")
        
        while True:
            col_input = input().strip().upper()
            if is_valid_column(col_input):
                col = ord(col_input) - ord('A')
                if place_checker(board, col, checker):
                    break
                else:
                    print("Column is full. Please enter another column: ")
            else:
                print("Invalid input. Please enter a valid column (A-G): ")
        
        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
