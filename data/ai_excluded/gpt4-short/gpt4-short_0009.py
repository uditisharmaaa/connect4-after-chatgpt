import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G"]
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 4  # Set between 2 and 5

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-" * (COLUMNS * 4 + 1))

# Drop a piece in a column
def drop_piece(board, column, marker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = marker
            return True
    return False

# Check for a win
def check_win(board, marker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == marker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == marker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Get player input
def get_player_input():
    while True:
        choice = input("Choose a column (A-G): ").strip().upper()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        print("Invalid column. Try again.")

# Main game loop
def play_game():
    # Setup
    board = create_board()
    players = PLAYER_MARKERS[:NUM_PLAYERS]
    random.shuffle(players)
    current_player_idx = 0

    while True:
        print_board(board)
        print(f"Player {players[current_player_idx]}'s turn")
        column = get_player_input()

        if drop_piece(board, column, players[current_player_idx]):
            # Check win
            if check_win(board, players[current_player_idx]):
                print_board(board)
                print(f"Player {players[current_player_idx]} wins!")
                break

            # Check draw
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print("Column is full. Try again.")

# Run the game
if __name__ == "__main__":
    play_game()
