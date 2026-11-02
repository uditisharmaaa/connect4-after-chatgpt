import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', 'C', ...]


def clear_screen():
    os.system('clear')


def create_board():
    """Create and initialize the Connect 4 game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current game board."""
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)


def get_valid_column_input(board):
    """Prompt the user for a valid column."""
    while True:
        user_input = input("Please enter a column: ").upper()
        if user_input in COLUMN_LABELS:
            col = COLUMN_LABELS.index(user_input)
            if board[0][col] == " ":
                return col
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")


def place_checker(board, col, checker):
    """Place the player's checker in the selected column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break


def check_winner(board, checker):
    """Check if the given player has won the game (4 in a row)."""
    # Horizontal Check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (
                board[row][col]
                == board[row + 1][col]
                == board[row + 2][col]
                == board[row + 3][col]
                == checker
            ):
                return True

    # Diagonal Check (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (
                board[row][col]
                == board[row + 1][col + 1]
                == board[row + 2][col + 2]
                == board[row + 3][col + 3]
                == checker
            ):
                return True

    # Diagonal Check (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (
                board[row][col]
                == board[row - 1][col + 1]
                == board[row - 2][col + 2]
                == board[row - 3][col + 3]
                == checker
            ):
                return True

    return False


def check_draw(board):
    """Check if the game board is full (draw)."""
    return all(cell != " " for row in board for cell in row)


def main():
    """Main game logic."""
    clear_screen()
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)

    print("Welcome to Connect 4!")
    print(f"Randomly choosing Player {CHECKERS[current_player_index]} to start.\n")
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player_index]}'s turn.")
        col = get_valid_column_input(board)
        place_checker(board, col, CHECKERS[current_player_index])
        clear_screen()
        print_board(board)

        if check_winner(board, CHECKERS[current_player_index]):
            print(f"Player {CHECKERS[current_player_index]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
