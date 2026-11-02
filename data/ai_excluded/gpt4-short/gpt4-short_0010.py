import random
import os

# Constants
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Adjustable number of players (from 2 to 5)

# Game settings: rows and columns
ROWS = 6
COLS = 7
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G"]

def create_board():
    """Create an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')  # Clear the terminal for a clean display
    print(" " + " ".join(COLUMN_LABELS))  # Print column labels (A-G)
    for row in board:  # Iterate through rows and print each one
        print("|" + "|".join(row) + "|")
    print("=" * (2 * COLS + 1))  # Draw a bottom border

def is_valid_column(column, board):
    """Check if a column label is valid and has space for a disc."""
    if column not in COLUMN_LABELS:
        return False
    col_index = COLUMN_LABELS.index(column)
    return board[0][col_index] == " "  # A valid column has space in the top row

def get_column_input(current_player, board):
    """Prompt the user for a column and validate their input."""
    while True:
        column = input(f"Player {current_player}, choose a column (A-G): ").upper().strip()
        if is_valid_column(column, board):
            return COLUMN_LABELS.index(column)  # Return the column index
        print("Invalid column. Try again.")

def drop_piece(board, col, player):
    """Drop a piece into the chosen column."""
    for row in reversed(board):  # Start from the bottom row and move up
        if row[col] == " ":
            row[col] = player
            break

def check_winner(board, player):
    """Check for a winning move for the given player."""
    # Check all directions: Horizontal, Vertical, and Diagonals
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and  # Horizontal
                all(board[r][c + i] == player for i in range(4))):
                return True
            if (r + 3 < ROWS and  # Vertical
                all(board[r + i][c] == player for i in range(4))):
                return True
            if (r + 3 < ROWS and c + 3 < COLS and  # Diagonal (/)
                all(board[r + i][c + i] == player for i in range(4))):
                return True
            if (r + 3 < ROWS and c - 3 >= 0 and  # Diagonal (\)
                all(board[r + i][c - i] == player for i in range(4))):
                return True
    return False

def check_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))  # Top row is full

def play_game():
    """Main function to run the Connect 4 game."""
    board = create_board()  # Initialize the game board
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Randomly select first player
    players = PLAYERS[:NUM_PLAYERS]  # Get the first NUM_PLAYERS characters
    print_board(board)

    while True:
        current_player = players[current_player_index]  # Get the current player
        col_index = get_column_input(current_player, board)  # Get valid column
        drop_piece(board, col_index, current_player)  # Drop the player's piece
        print_board(board)  # Display updated board
        
        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break
        
        # Check for a draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Proceed to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
