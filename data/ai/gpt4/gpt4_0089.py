import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "
COLUMN_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Initialize the board
def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(COLUMN_LABELS[:COLUMNS]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")
    print()

# Check for a valid column
def is_valid_column(col, board):
    if col < 0 or col >= COLUMNS:  # Out of bounds
        return False
    return board[0][col] == EMPTY  # Check if column is not full

# Get the first empty row in a column
def get_empty_row(col, board):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return -1

# Check for a win
def check_win(board, player):
    # Horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical win
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal (down-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal (down-left) win
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != EMPTY for row in board for cell in row)

# Main game function
def play_game():
    # Initialize game state
    board = create_board()
    players = 2  # Fixing to 2 players as per submission guidelines
    player_symbols = CHECKERS[:players]
    current_player = random.randint(0, players - 1)  # Random start

    # Start the game loop
    while True:
        print_board(board)
        print(f"Player {player_symbols[current_player]}'s turn.")
        column = input("Please enter a column: ").strip().upper()

        # Check for valid input
        if len(column) != 1 or column not in COLUMN_LABELS[:COLUMNS]:
            print("Invalid input! Please enter a valid column letter.")
            continue

        col_index = COLUMN_LABELS.index(column)

        # Check if the column is valid
        if not is_valid_column(col_index, board):
            print("Invalid column! The column is full or out of bounds.")
            continue

        # Place the checker
        row = get_empty_row(col_index, board)
        board[row][col_index] = player_symbols[current_player]

        # Check for win
        if check_win(board, player_symbols[current_player]):
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % players

# Run the game
if __name__ == "__main__":
    play_game()
