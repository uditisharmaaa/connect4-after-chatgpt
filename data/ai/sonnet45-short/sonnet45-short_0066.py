import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """
    Creates and returns an empty game board.
    The board is a 2D list with ROWS rows and COLS columns.
    Empty cells are represented by '.'
    """
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """
    Displays the current game board with column labels.
    Prints from top to bottom (row 0 is the top of the board).
    """
    print("\n  " + " ".join(COLUMN_LABELS))  # Print column labels
    print("  " + "-" * (COLS * 2 - 1))  # Print separator line
    
    # Print each row with a row number
    for i, row in enumerate(board):
        print(f"{i} |" + "|".join(row) + "|")
    
    print("  " + "-" * (COLS * 2 - 1))  # Print bottom separator
    print()

def drop_piece(board, col, symbol):
    """
    Drops a piece into the specified column.
    The piece falls to the lowest available row in that column.
    Returns True if successful, False if column is full.
    """
    # Start from the bottom row and work upward
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == '.':
            board[row][col] = symbol
            return True
    return False  # Column is full

def is_valid_column(board, col):
    """
    Checks if a column index is valid and has space for a piece.
    Returns True if the column exists and isn't full.
    """
    if col < 0 or col >= COLS:
        return False
    # Check if top row of the column is empty
    return board[0][col] == '.'

def check_win(board, symbol):
    """
    Checks if the specified player has won the game.
    Checks all possible winning combinations: horizontal, vertical, and diagonal.
    Returns True if the player has 4 in a row.
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row - 1][col + 1] == symbol and
                board[row - 2][col + 2] == symbol and
                board[row - 3][col + 3] == symbol):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    return False

def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    Returns True if no empty cells remain in the top row.
    """
    return all(board[0][col] != '.' for col in range(COLS))

def get_player_input(player_symbol):
    """
    Gets and validates player input for column selection.
    Accepts column letters (A-G) or full column names.
    Returns the column index (0-6) or -1 for invalid input.
    """
    user_input = input(f"Player {player_symbol}, choose a column (A-G): ").strip().upper()
    
    # Check if input is a valid column label
    if user_input in COLUMN_LABELS:
        return COLUMN_LABELS.index(user_input)
    
    return -1  # Invalid input

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    Handles player turns, input validation, win/draw checking, and display.
    """
    # Get number of players
    while True:
        try:
            num_players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                break
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Set up players with their symbols
    players = PLAYER_SYMBOLS[:num_players]
    
    # Initialize the game board
    board = create_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    print(f"\nPlayers: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start the game...")
    
    # Main game loop
    while True:
        os.system('clear')  # Clear the screen for a clean display
        
        current_symbol = players[current_player_index]
        print_board(board)
        
        # Get valid input from current player
        while True:
            col_index = get_player_input(current_symbol)
            
            if col_index == -1:
                print("Invalid column. Please choose A-G.")
                continue
            
            if not is_valid_column(board, col_index):
                print("Column is full or invalid. Choose another column.")
                continue
            
            break  # Valid input received
        
        # Drop the piece into the chosen column
        drop_piece(board, col_index, current_symbol)
        
        # Check if current player won
        if check_win(board, current_symbol):
            os.system('clear')
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check if the board is full (draw)
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players

def main():
    """
    Entry point of the program.
    Allows players to play multiple games.
    """
    print("=" * 40)
    print("      Welcome to Connect 4!")
    print("=" * 40)
    print("\nRules: Get 4 in a row to win!")
    print("(horizontal, vertical, or diagonal)\n")
    
    while True:
        play_game()
        
        # Ask if players want to play again
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

# Run the game
if __name__ == "__main__":
    main()
