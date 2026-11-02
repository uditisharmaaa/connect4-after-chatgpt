import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


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
    for col in range(COLS):
        label = chr(65 + col)  # Convert 0->A, 1->B, etc.
        print(label + "   ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def get_column_input(player_checker):
    """Get and return valid column input from player."""
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if it's a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65  # A->0, B->1, etc.
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print("Invalid input. Column out of range.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """Place checker in the specified column. Return True if successful, False if column is full."""
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the given checker has won. Return True if won, False otherwise."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw). Return True if draw, False otherwise."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def main():
    """Main game loop."""
    # Create board
    board = create_board()
    
    # Create list of player checkers
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        current_checker = players[current_player_index]
        
        # Get column input
        col = get_column_input(current_checker)
        
        # Place checker
        if place_checker(board, col, current_checker):
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
        else:
            # Column is full, player loses turn
            print("Column is full. You lose your turn.")
            print_board(board)
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    main()
