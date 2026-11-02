import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checker symbols for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))  # Column headers A, B, C, ...
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def is_valid_column(column, board):
    """Checks if a column choice is valid."""
    if column < 0 or column >= COLUMNS or board[0][column] != " ":
        return False
    return True

def find_row(column, board):
    """Finds the lowest available row in a column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

def place_checker(column, checker, board):
    """Places a checker in a valid column."""
    row = find_row(column, board)
    if row is not None:
        board[row][column] = checker
        return True
    return False

def check_four(start_row, start_col, d_row, d_col, board, checker):
    """Checks if there are 4 consecutive checkers in a given direction."""
    count = 0
    for i in range(4):
        r = start_row + i * d_row
        c = start_col + i * d_col
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def check_winner(board, checker):
    """Checks if the given checker has won the game."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                # Check horizontal, vertical, and two diagonal directions
                if (check_four(row, col, 0, 1, board, checker) or  # Horizontal
                    check_four(row, col, 1, 0, board, checker) or  # Vertical
                    check_four(row, col, 1, 1, board, checker) or  # Diagonal /
                    check_four(row, col, 1, -1, board, checker)): # Diagonal \
                    return True
    return False

def check_draw(board):
    """Checks if the board is completely filled, resulting in a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_player_input(player, board):
    """Prompts the player for a valid column input."""
    while True:
        column_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column_input) == 1 and column_input.isalpha():
            column = ord(column_input) - ord('A')
            if is_valid_column(column, board):
                return column
        print("Invalid input. Try again.")

def main():
    """Main function to run the Connect 4 game."""
    # Initialize the board and players
    board = create_board()
    player_symbols = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select first player

    print_board(board)

    while True:
        # Current player's turn
        player_symbol = player_symbols[current_player]
        column = get_player_input(player_symbol, board)
        place_checker(column, player_symbol, board)
        print_board(board)

        # Check for win or draw
        if check_winner(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
