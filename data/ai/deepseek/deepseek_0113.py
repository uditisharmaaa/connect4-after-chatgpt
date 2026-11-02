import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print board rows
    for row in board:
        print("+" + "---+".join([""] * (COLS + 1)))
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    # Print bottom border
    print("+" + "---+".join([""] * (COLS + 1)))

def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col > chr(65 + COLS - 1):
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
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

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row-1][col+1] == checker and
                board[row-2][col+2] == checker and
                board[row-3][col+3] == checker):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    global current_player
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        col = get_valid_column()
        if not place_checker(board, col, current_player):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
