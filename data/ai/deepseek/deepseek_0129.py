import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board to the console."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels
    col_labels = "  " + "   ".join([chr(65 + i) for i in range(COLS)]) + "  "
    print(col_labels)
    
    # Print the top border
    print("+" + ("---+" * COLS))
    
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + ("---+" * COLS))

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    char = column.upper()
    if char < 'A' or char > chr(65 + COLS - 1):
        return False
    return True

def get_player_input(player):
    """Get and validate player input."""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if is_valid_column(column):
            return ord(column) - ord('A')
        else:
            print("Invalid input. Please enter a valid column (A-{}).".format(chr(65 + COLS - 1)))

def place_checker(board, column, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col + 1] == player and 
                board[row][col + 2] == player and 
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row + 1][col] == player and 
                board[row + 2][col] == player and 
                board[row + 3][col] == player):
                return True
    
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row + 1][col + 1] == player and 
                board[row + 2][col + 2] == player and 
                board[row + 3][col + 3] == player):
                return True
    
    # Check diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row - 1][col + 1] == player and 
                board[row - 2][col + 2] == player and 
                board[row - 3][col + 3] == player):
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
    board = initialize_board()
    players = SYMBOLS[:PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        
        column = get_player_input(current_player)
        
        if not place_checker(board, column, current_player):
            print("Column is full. You lose your turn.")
        else:
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("Game is a draw!")
                break
        
        # Switch players
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
