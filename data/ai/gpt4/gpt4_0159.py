import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal window."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    columns = "  ".join(chr(65 + i) for i in range(COLS))
    print(f"  {columns}")
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Checks if the given column (letter) is valid."""
    if column not in range(0, COLS):
        return False
    return board[0][column] == " "

def drop_checker(board, column, symbol):
    """Drops the checker in the given column with the player's symbol."""
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return row

def check_win(board, row, col, symbol):
    """Checks for a win starting from the specified row and column."""
    def count_in_direction(dx, dy):
        count = 0
        x, y = row, col
        while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == symbol:
            count += 1
            x += dx
            y += dy
        return count - 1

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        if count_in_direction(dx, dy) + count_in_direction(-dx, -dy) >= 3:
            return True
    return False

def is_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(board[0][col] != " " for col in range(COLS))

def get_valid_column(board, player, player_symbol):
    """Prompts the player for a valid column and validates the input."""
    while True:
        try:
            column_letter = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
            if len(column_letter) != 1 or not column_letter.isalpha():
                raise ValueError("Invalid input! Enter a single letter (e.g., A, B, C).")
            column = ord(column_letter) - ord('A')
            if not (0 <= column < COLS):
                raise ValueError(f"Invalid column! Enter a letter between A and {chr(64 + COLS)}.")
            if not is_valid_column(column, board):
                raise ValueError("Column is full! Choose another one.")
            return column
        except ValueError as e:
            print(e)

def play_game():
    """Main function to manage the game flow."""
    # Initialize game
    board = create_board()
    num_players = MIN_PLAYERS  # Changeable for more players, e.g., set this to 3 or 4 for testing
    player_symbols = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    clear_screen()
    print("Welcome to Connect 4!")
    print_board(board)

    # Game loop
    while True:
        current_symbol = player_symbols[current_player_index]
        column = get_valid_column(board, current_player_index + 1, current_symbol)
        row = drop_checker(board, column, current_symbol)

        clear_screen()
        print_board(board)

        if check_win(board, row, column, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    play_game()
