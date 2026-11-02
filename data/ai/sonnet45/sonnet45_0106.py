import random
import os

# Global constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    The board has ROWS rows and COLS columns.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels and borders.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border of each cell
        print("  ", end="")
        for col in range(COLS):
            print("+---", end="")
        print("+")
        
        # Print cell contents
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  ", end="")
    for col in range(COLS):
        print("+---", end="")
    print("+")


def get_column_input(player_checker):
    """
    Prompts the player to enter a column and validates the input.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col_index, player_checker):
    """
    Places a checker in the specified column at the lowest available row.
    Returns True if placement was successful, False if column is full.
    """
    # Start from the bottom row and work upward
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    
    # Column is full
    return False


def check_win(board, player_checker):
    """
    Checks if the given player has won the game.
    Returns True if player has 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if all cells are occupied.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def main():
    """
    Main game loop for Connect 4.
    """
    # Create the board
    board = create_board()
    
    # Get player checkers based on number of players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get column input from player
        col_index = get_column_input(current_player)
        
        # Try to place the checker
        if place_checker(board, col_index, current_player):
            # Print updated board
            print_board(board)
            
            # Check if current player won
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column is full, player loses turn
            print("Column is full. You lose your turn.")
            print_board(board)
            
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    main()
