import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of possible player checkers in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return a new empty board with given dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels (A, B, C, etc.)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print the board rows with separators
    for row in board:
        horizontal_line = "+" + ("---+" * COLS)
        print(horizontal_line)
        print("| " + " | ".join(row) + " |")
    
    print("+" + "---+" * COLS)

def get_player_checkers():
    """Return the list of player checkers based on number of players."""
    return PLAYER_CHECKERS[:NUM_PLAYERS]

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    return 0 <= col < COLS and board[0][col] == " "

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_win(board, checker):
    """Check if the specified checker has won (horizontal, vertical, or diagonal)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True

    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True

    # Check diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(board, player_checker):
    """Get and validate player input for column selection."""
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if len(choice) != 1 or not choice.isalpha():
            print("Please enter a single letter (A-G).")
            continue
        
        col = ord(choice) - ord('A')
        
        if not (0 <= col < COLS):
            print(f"Please enter a column letter from A to {chr(ord('A') + COLS - 1)}")
            continue
        
        if not is_valid_move(board, col):
            print("That column is full. Please choose another column.")
            continue
            
        return col

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    player_checkers = get_player_checkers()
    
    # Randomly choose starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = player_checkers[current_player]
        col = get_player_input(board, player_checker)
        place_checker(board, col, player_checker)
        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
