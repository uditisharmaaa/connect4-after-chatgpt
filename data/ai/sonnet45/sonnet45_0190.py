import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with all spaces initialized to whitespace."""
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
    
    # Print column letters
    print("  ", end="")
    for i in range(NUM_COLS):
        col_letter = chr(65 + i)  # 65 is ASCII for 'A'
        print(col_letter + "   ", end="")
    print()
    
    # Print board rows
    for row in range(NUM_ROWS):
        # Print top border
        print("+---" * NUM_COLS + "+")
        
        # Print row content
        print("| ", end="")
        for col in range(NUM_COLS):
            print(board[row][col] + " | ", end="")
        print()
    
    # Print bottom border
    print("+---" * NUM_COLS + "+")

def get_valid_input(player_checker):
    """Get and validate player input for column selection."""
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is empty
        if len(user_input) == 0:
            print("Invalid input. Please enter a column letter.")
            continue
        
        # Get first character and convert to uppercase
        col_char = user_input[0].upper()
        
        # Check if it's a valid letter
        if col_char < 'A' or col_char > chr(65 + NUM_COLS - 1):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(col_char) - 65
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful, False if column is full."""
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal wins (down-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal wins (down-left)
    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLS):
            if (board[row][col] == checker and 
                board[row + 1][col - 1] == checker and 
                board[row + 2][col - 2] == checker and 
                board[row + 3][col - 3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    # Initialize the board
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get valid column input
        col = get_valid_input(player_checker)
        
        # Try to place the checker
        if place_checker(board, col, player_checker):
            # Print the updated board
            print_board(board)
            
            # Check if current player won
            if check_win(board, player_checker):
                print("Player " + player_checker + " won!")
                game_over = True
            # Check for draw
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                # Move to next player
                current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Column was full, player loses turn
            print("Column is full! You lose your turn.")
            print_board(board)
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
main()
