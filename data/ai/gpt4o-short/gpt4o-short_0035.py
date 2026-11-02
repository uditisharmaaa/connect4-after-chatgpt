import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Define player symbols here
NUM_PLAYERS = 3  # You can set this from 2 to 5

# Initialize the game board
def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Clear the terminal
def clear_screen():
    os.system('clear')  # Use 'cls' if you are on Windows

# Display the board
def display_board(board):
    clear_screen()
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (2 * COLUMNS + 1))

# Get the column index based on the label
def get_column_index(label):
    return COLUMN_LABELS.index(label)

# Drop a piece in the board
def drop_piece(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return True
    return False

# Check for a win condition
def check_win(board, symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + offset] == symbol for offset in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + offset][col] == symbol for offset in range(4)):
                return True

    # Positive diagonal check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - offset][col + offset] == symbol for offset in range(4)):
                return True

    # Negative diagonal check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + offset][col + offset] == symbol for offset in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def main():
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))

    while True:
        display_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}'s turn")

        # Validate input
        while True:
            try:
                move = input(f"Choose a column ({COLUMN_LABELS}): ").strip().upper()
                if move not in COLUMN_LABELS:
                    raise ValueError("Invalid column. Try again.")
                if not drop_piece(board, get_column_index(move), player_symbol):
                    raise ValueError("Column is full. Try again.")
                break
            except ValueError as e:
                print(e)

        # Check for win
        if check_win(board, player_symbol):
            display_board(board)
            print(f"Player {player_symbol} wins!")
            break

        # Check for draw
        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
