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
    """Print the current board state."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board rows
    for row in range(ROWS):
        # Print top border
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()


def get_column_input(player_checker):
    """Get and validate column input from player."""
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is within board bounds
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(64 + COLS) + ".")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful, False if column is full."""
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            win = True
            for i in range(WIN_LENGTH):
                if board[row][col + i] != checker:
                    win = False
                    break
            if win:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            win = True
            for i in range(WIN_LENGTH):
                if board[row + i][col] != checker:
                    win = False
                    break
            if win:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            win = True
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] != checker:
                    win = False
                    break
            if win:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            win = True
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] != checker:
                    win = False
                    break
            if win:
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get column input
        col = get_column_input(checker)
        
        # Place checker
        success = place_checker(board, col, checker)
        
        if not success:
            print("Column is full! You lose your turn.")
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


# Start the game
play_game()
