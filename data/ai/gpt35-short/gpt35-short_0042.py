import os
import random

# Constants for the game setup

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Player tokens to be used - can play 2 to 5 players
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen using os.system('clear')."""
    os.system('clear')  # On Windows, use 'cls'

def create_board():
    """Create an empty board with ROWS x COLS."""
    # We'll use a list of lists filled with spaces to represent empty cells
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board to the screen with column labels."""
    # Print column labels
    print(" " + "   ".join(COLUMN_LABELS))
    # Print each row
    for row in range(ROWS):
        # Print each cell separated by '|'
        print("| " + " | ".join(board[row]) + " |")
    # Print a bottom line
    print("-" * (COLS * 4 + 1))

def get_player_count():
    """Prompt the user to select how many players will be playing."""
    while True:
        try:
            num = int(input(f"Enter number of players (2 to 5): "))
            if 2 <= num <= 5:
                return num
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_move(player_token, board):
    """Prompt the player to enter a valid column to drop their token."""
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper().strip()
        if move not in COLUMN_LABELS:
            print("Invalid column. Please enter a letter from A to G.")
            continue
        col = COLUMN_LABELS.index(move)
        # Check if the column is full
        if board[0][col] != ' ':
            print("That column is full. Choose a different one.")
            continue
        return col

def drop_token(board, col, token):
    """Drop the player's token into the chosen column."""
    # Start from the bottom row and find the first empty cell
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col  # Return the position where token landed

def check_win(board, row, col, token):
    """Check if placing token at (row, col) causes a win."""

    def count_tokens(delta_row, delta_col):
        """Count continuous tokens matching 'token' in a direction."""
        r, c = row + delta_row, col + delta_col
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check all directions: horizontal, vertical, and two diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        # Count tokens in the positive direction + negative direction + 1 (current token)
        total = 1 + count_tokens(dr, dc) + count_tokens(-dr, -dc)
        if total >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    # If top row has no empty spaces, the board is full
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!\n")

    # Get number of players
    num_players = get_player_count()
    players = PLAYER_TOKENS[:num_players]

    # Choose random first player
    current_player_index = random.randint(0, num_players - 1)

    # Create the game board
    board = create_board()

    # Main game loop
    while True:
        clear_screen()
        print_board(board)
        current_token = players[current_player_index]

        # Get player move
        col = get_move(current_token, board)
        row, col = drop_token(board, col, current_token)

        # Check for win
        if check_win(board, row, col, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more moves possible.")
            break

        # Move to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
