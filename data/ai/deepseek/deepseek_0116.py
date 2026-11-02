import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# List of possible player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    headers = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(headers))
    
    horizontal_line = "+" + ("---+" * COLS)
    print(horizontal_line)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(horizontal_line)

def get_random_first_player():
    """Return a random player index to start the game."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    char = column.upper()
    return 'A' <= char <= chr(ord('A') + COLS - 1)

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
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
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    print(f"Player {players[current_player]} starts first!")
    input("Press Enter to continue...")
    
    while True:
        os.system('clear')
        print_board(board)
        
        checker = players[current_player]
        print(f"Player {checker}, please enter a column: ")
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid column. Please enter a letter from A to " + chr(ord('A') + COLS - 1))
            input("Press Enter to continue...")
            continue
        
        col_index = ord(col) - ord('A')
        if board[0][col_index] != " ":
            print("Column is full. You lose this turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        if not place_checker(board, col, checker):
            print("Column is full. You lose this turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        if check_win(board, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
