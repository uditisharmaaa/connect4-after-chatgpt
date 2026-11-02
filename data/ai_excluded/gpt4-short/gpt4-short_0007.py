import os
import random

# Constants: Set up the game
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G"]
NUM_PLAYERS = 3  # Change this to 2, 3, 4, or 5
PLAYER_MARKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    print(" " + " ".join(COLUMN_LABELS))  # Print column labels
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLUMNS * 2 + 1))  # Bottom border

def is_valid_column(board, col_index):
    """Checks if a column is valid (not full)."""
    return board[0][col_index] == " "

def get_next_open_row(board, col_index):
    """Finds the next open row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return None

def drop_piece(board, row, col, piece):
    """Drops the player's piece into the board at the specified row and column."""
    board[row][col] = piece

def check_win(board, piece):
    """Checks if the specified player has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(board[0][c] != " " for c in range(COLUMNS))

def get_player_choice(board, player):
    """Prompts the player and validates input."""
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").strip().upper()
        if choice in COLUMN_LABELS:
            col_index = COLUMN_LABELS.index(choice)
            if is_valid_column(board, col_index):
                return col_index
            else:
                print("Column is full. Try again.")
        else:
            print("Invalid input. Please choose a column (A-G).")

def play_game():
    """Main function to play the Connect 4 game."""
    # Initialize the game
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    print_board(board)
    print(f"Randomly selected Player {PLAYER_MARKERS[current_player_index]} to go first!")

    while not game_over:
        # Current player's turn
        player = PLAYER_MARKERS[current_player_index]
        col_index = get_player_choice(board, player)
        row = get_next_open_row(board, col_index)
        drop_piece(board, row, col_index, player)

        print_board(board)

        # Check for win or draw
        if check_win(board, player):
            print(f"Player {player} wins! Congratulations!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
