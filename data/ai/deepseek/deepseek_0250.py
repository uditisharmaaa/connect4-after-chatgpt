import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize an empty game board with ROWS rows and COLS columns."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print("+" + "---+" * COLS)
    
    # Print each row
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * COLS)

def is_valid_column(column):
    """Check if the column input is valid (uppercase letter within range)."""
    if len(column) != 1:
        return False
    col_num = ord(column) - ord('A')
    return 0 <= col_num < COLS

def place_checker(board, column, checker):
    """Place the checker in the specified column at the lowest available row."""
    col_num = ord(column) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_num] == " ":
            board[row][col_num] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the specified checker has won (4 in a row)."""
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
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ")
        
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column (A to" + f" {chr(65 + COLS - 1)}).")
            continue
        
        if not place_checker(board, column, checker):
            print("Column is full! You lose your turn.")
        else:
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
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
