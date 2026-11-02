import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the board
    for row in board:
        print("+" + "---+" * COLS)
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    # Print the bottom border
    print("+" + "---+" * COLS)

def get_player_checkers(num_players):
    """Return the list of player checkers based on number of players."""
    checkers = ["X", "O", "V", "H", "M"]
    return checkers[:num_players]

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if not col or len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter (A-{0}).".format(chr(65 + COLS - 1)))
            continue
        
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        if board[0][col_num] != " ":
            print("Column is full. Choose another column.")
            continue
        
        return col_num

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest empty row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won the game."""
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
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
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
    for row in board:
        if " " in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    global current_player
    
    board = initialize_board()
    player_checkers = get_player_checkers(PLAYERS)
    current_player = random.choice(range(PLAYERS))
    
    print_board(board)
    
    while True:
        checker = player_checkers[current_player]
        col = get_valid_column(board)
        place_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
