import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(NUM_COLS):
        label = chr(ord('A') + col)
        print(label + "   ", end="")
    print()
    
    # Print board rows
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * NUM_COLS + "+")

def get_player_move(player_checker):
    """Get and validate player input."""
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        move = move.upper()
        
        # Check if it's a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(move) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= NUM_COLS:
            print("Invalid input. Column out of range.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column. Returns True if successful, False if column is full."""
    # Start from bottom row and go up
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (down-left)
    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLS):
            if (board[row][col] == checker and
                board[row + 1][col - 1] == checker and
                board[row + 2][col - 2] == checker and
                board[row + 3][col - 3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
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
        # Get current player's checker
        current_checker = CHECKERS[current_player_index]
        
        # Get player move
        col = get_player_move(current_checker)
        
        # Place checker
        if not place_checker(board, col, current_checker):
            print("Column is full! You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    main()
