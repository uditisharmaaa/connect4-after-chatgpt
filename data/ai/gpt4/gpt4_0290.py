import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and returns an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_column):
    """Checks if the given column input is valid."""
    return len(input_column) == 1 and input_column.isalpha() and "A" <= input_column <= chr(65 + COLUMNS - 1)

def get_column_index(column_letter):
    """Converts the column letter to a zero-based column index."""
    return ord(column_letter.upper()) - 65

def is_column_full(board, column):
    """Checks if a column is full."""
    return board[0][column] != " "

def drop_checker(board, column, checker):
    """Drops the checker's symbol in the specified column."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom of the column
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_win(board, row, col, checker):
    """Checks if placing a checker at (row, col) creates a win."""
    # Directions: (row_step, col_step)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal /
    for d_row, d_col in directions:
        count = 1  # Include the current checker
        for delta in (-1, 1):  # Check both directions
            r, c = row, col
            while True:
                r += delta * d_row
                c += delta * d_col
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    break
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    """Main function to run the Connect 4 game."""
    # Game initialization
    board = create_board()
    checkers_list = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        # Get current player's checker and prompt input
        checker = checkers_list[current_player]
        print(f"Player {checker}, please enter a column:")

        while True:
            input_column = input("> ").strip().upper()
            if not is_valid_input(input_column):
                print("Invalid input. Please enter a valid column (A-G).")
                continue

            column_index = get_column_index(input_column)
            if is_column_full(board, column_index):
                print("Column is full. Please choose another column.")
            else:
                break

        # Place the checker in the selected column
        drop_row = next(row for row in range(ROWS - 1, -1, -1) if board[row][column_index] == " ")
        drop_checker(board, column_index, checker)

        # Print updated board
        print_board(board)

        # Check for a win
        if check_win(board, drop_row, column_index, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
