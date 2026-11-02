import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def clear_screen():
    """Clears the screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates and returns an empty Connect 4 board."""
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    column_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print("  " + column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if the selected column is valid for a move."""
    return column.isalpha() and 'A' <= column <= 'Z' and ord(column) - ord('A') < len(board[0])

def is_column_full(column_index, board):
    """Checks if the selected column is full."""
    return board[0][column_index] != EMPTY_CELL

def drop_checker(column_index, player_symbol, board):
    """Drops the player's checker into the selected column."""
    for row in reversed(board):
        if row[column_index] == EMPTY_CELL:
            row[column_index] = player_symbol
            break

def check_win(board, player_symbol):
    """Checks if the player has won (horizontal, vertical, diagonal)."""
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for row in board:
        for col in range(columns - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != EMPTY_CELL for col in range(len(board[0])))

def get_valid_column(player_symbol, board):
    """Prompts the player to select a valid column."""
    while True:
        column = input(f"Player {player_symbol}, please enter a column: ").upper()
        if not is_valid_column(column, board):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column_index = ord(column) - ord('A')
        if is_column_full(column_index, board):
            print("Column is full. Choose another column.")
            continue

        return column_index

def play_game():
    """Main function to run the Connect 4 game."""
    # Initialization
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Can be changed to any number between 2 and MAX_PLAYERS
    player_symbols = PLAYER_SYMBOLS[:num_players]
    random.shuffle(player_symbols)
    current_player_index = 0
    print_board(board)

    while True:
        # Get the current player's symbol
        current_player = player_symbols[current_player_index]

        # Get valid column and drop the checker
        column_index = get_valid_column(current_player, board)
        drop_checker(column_index, current_player, board)
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    play_game()
