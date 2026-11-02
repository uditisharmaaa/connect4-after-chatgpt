import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Change this to 3, 4, or 5 for additional players
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create a game board with given dimensions."""
    return [[" "] * columns for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column headers
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(column, board):
    """Check if the input column is valid."""
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

def drop_checker(board, column, checker):
    """Drop the player's checker into the specified column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_winner(board, checker):
    """Check if the given checker has achieved a Connect 4."""
    # Check horizontally
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col+4] == [checker] * 4:
                return True

    # Check vertically
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonally (/ direction)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    # Check diagonally (\ direction)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    clear_screen()
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {current_player}, please enter a column:")

        column = input("> ").strip()
        if not is_valid_input(column, board):
            print("Invalid input, please try again.")
            input("Press Enter to continue...")
            continue

        drop_checker(board, column, current_player)

        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % len(players)]

if __name__ == "__main__":
    main()
