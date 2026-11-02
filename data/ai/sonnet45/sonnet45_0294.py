import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_valid_input(player_symbol):
    """Get valid column input from player."""
    while True:
        column_input = input("Player " + player_symbol + ", please enter a column: ")
        
        # Check if input is a single character
        if len(column_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is uppercase letter
        if not column_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column number
        col = ord(column_input) - 65
        
        # Check if column is within board range
        if col < 0 or col >= COLS:
            print("Invalid input. Column out of range.")
            continue
        
        return col

def place_checker(board, col, player_symbol):
    """Place a checker in the specified column. Return True if successful, False if column is full."""
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return True
    return False

def check_win(board, player_symbol):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col - i] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    """Main game function."""
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        player_symbol = PLAYER_SYMBOLS[current_player_index]
        
        # Get valid column from player
        col = get_valid_input(player_symbol)
        
        # Place checker
        success = place_checker(board, col, player_symbol)
        
        if not success:
            print("Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, player_symbol):
            print("Player " + player_symbol + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
main()
