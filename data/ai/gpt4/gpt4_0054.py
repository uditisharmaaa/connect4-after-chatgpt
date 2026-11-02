import os
import random

# Global Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]  # Adjusted for the number of players

def create_board():
    """Creates an empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')  # Clear console
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def drop_checker(board, column, checker):
    """Drops the checker into the selected column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def is_valid_column(column_input):
    """Checks if the input column is valid."""
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column = ord(column_input.upper()) - 65
    return 0 <= column < COLUMNS

def is_column_full(board, column):
    """Checks if the column is full."""
    return board[0][column] != " "

def check_for_win(board, checker):
    """Checks if the player has won with 4 in a row."""
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal check (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal check (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    """Checks if the board is full and the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    """Main function to run the game."""
    # Initialize game variables
    board = create_board()
    current_player_idx = random.randint(0, MAX_PLAYERS - 1)
    turn_count = 0

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_idx]} goes first!")

    # Main game loop
    while True:
        player_checker = PLAYER_CHECKERS[current_player_idx]
        print_board(board)

        # Getting valid column input from the player
        while True:
            column_input = input(f"Player {player_checker}, please enter a column: ").strip()
            if is_valid_column(column_input):
                column = ord(column_input.upper()) - 65
                if not is_column_full(board, column):
                    break
                else:
                    print("Column is full. Try again.")
            else:
                print("Invalid input. Please enter a valid column (A-G).")

        # Drop the checker into the board
        drop_checker(board, column, player_checker)

        # Checking for a win
        if check_for_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Checking for a draw
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_idx = (current_player_idx + 1) % MAX_PLAYERS
        turn_count += 1

if __name__ == "__main__":
    main()
