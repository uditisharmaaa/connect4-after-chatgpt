import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create and initialize the game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column(board):
    """Prompt the user to input a valid column. Keep prompting until input is valid."""
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input < chr(65 + COLUMNS):
            col = ord(col_input) - 65
            if board[0][col] == " ":
                return col
            else:
                print("Column is full. Please choose another one.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, player):
    """Drop the player's checker into the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            break

def check_winner(board, player):
    """Check if the given player has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    """Run the Connect 4 game."""
    # Initialize game state
    board = create_board()
    num_players = 2   # Fixed to 2 players for submission; can be adjusted to MAX_PLAYERS
    players = PLAYERS[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        chosen_col = get_valid_column(board)
        drop_checker(board, chosen_col, players[current_player_index])

        # Check for a win
        if check_winner(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Alternate to the next player
        current_player_index = (current_player_index + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
