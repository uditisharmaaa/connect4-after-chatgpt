import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    """Clears the console screen."""
    os.system("clear")

def initialize_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if the given column is valid and not full."""
    if not column.isalpha() or len(column) != 1:
        return False
    col_index = ord(column.upper()) - 65
    if col_index < 0 or col_index >= COLUMNS:
        return False
    return board[0][col_index] == " "

def drop_checker(column, player_token, board):
    """Drops a checker for the given player into the chosen column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player_token
            return True
    return False

def check_winner(board, player_token):
    """Checks if the given player has won the game."""
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [player_token] * 4:
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + offset][col] == player_token for offset in range(4)):
                return True

    # Diagonal (\) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + offset][col + offset] == player_token for offset in range(4)):
                return True

    # Diagonal (/) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - offset][col + offset] == player_token for offset in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game board and select starting player
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        print(f"Player {PLAYER_TOKENS[current_player]}'s turn.")
        column = input("Please enter a column: ").strip()

        if not is_valid_column(column, board):
            print("Invalid column. Try again.")
            continue

        drop_checker(column, PLAYER_TOKENS[current_player], board)

        print_board(board)

        if check_winner(board, PLAYER_TOKENS[current_player]):
            print(f"Player {PLAYER_TOKENS[current_player]} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
