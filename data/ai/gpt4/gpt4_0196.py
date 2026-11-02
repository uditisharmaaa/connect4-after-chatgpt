import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty game board with given rows and columns."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_column_valid(board, col):
    """Checks if a column is valid and has space available."""
    return col in COLUMN_LABELS and any(row[COLUMN_LABELS.index(col)] == " " for row in board)

def get_valid_column_input(board):
    """Gets a valid column input from the user."""
    while True:
        col = input("Please enter a column: ").strip().upper()
        if is_column_valid(board, col):
            return col
        else:
            print("Invalid input. Please try again.")

def drop_checker(board, col, marker):
    """Drops a checker into the specified column."""
    column_index = COLUMN_LABELS.index(col)
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = marker
            return

def is_winner(board, marker):
    """Checks if the given player (marker) has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == marker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == marker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == marker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (board completely filled)."""
    return all(row[col] != " " for row in board for col in range(COLUMNS))

def main():
    # Setup game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed to 2 players as per assignment
    players = [PLAYER_MARKERS[i] for i in range(num_players)]
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    # Game loop
    while True:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}, it is your turn.")

        # Get valid input and place checker
        column = get_valid_column_input(board)
        drop_checker(board, column, current_player)

        # Check for win or draw
        if is_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
