import random
import os

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Maximum 5 players
PLAYER_COUNT = 2  # Change this to set the number of players (between 2 and 5)

# Functions
def initialize_board():
    """Initialize the game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def display_board(board):
    """Display the game board."""
    os.system('clear')  # Clear the screen
    print('  '.join(COLUMN_LABELS))  # Print column labels
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print()

def drop_piece(board, column, player):
    """Drop a piece into the chosen column."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # If column is full

def is_valid_column(column_input):
    """Check if the column input is valid."""
    return column_input in COLUMN_LABELS

def get_column_index(column_input):
    """Convert column label to index."""
    return COLUMN_LABELS.index(column_input)

def is_winner(board, player):
    """Check if the player has connected 4 pieces."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (/ direction)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_next_player(current_player_index, total_players):
    """Get the next player's index."""
    return (current_player_index + 1) % total_players

def play_game():
    """Main function to play the game."""
    # Set up the game
    board = initialize_board()
    total_players = max(2, min(PLAYER_COUNT, len(PLAYERS)))  # Clamp the number of players
    players = PLAYERS[:total_players]
    current_player_index = random.randint(0, total_players - 1)  # Randomize first player
    winner = None

    while True:
        display_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn!")

        # Get valid input
        while True:
            column_input = input("Choose a column (A-G): ").strip().upper()
            if not is_valid_column(column_input):
                print("Invalid column. Please choose a valid column (A-G).")
                continue
            column_index = get_column_index(column_input)
            if board[0][column_index] != ' ':
                print("Column is full. Please choose a different one.")
                continue
            break

        # Drop the piece and check for a win or draw
        drop_piece(board, column_index, current_player)
        if is_winner(board, current_player):
            winner = current_player
            break
        if is_draw(board):
            break

        # Move to the next player
        current_player_index = get_next_player(current_player_index, total_players)

    # Game over
    display_board(board)
    if winner:
        print(f"Player {winner} wins!")
    else:
        print("It's a draw!")

# Run the game
if __name__ == "__main__":
    play_game()
