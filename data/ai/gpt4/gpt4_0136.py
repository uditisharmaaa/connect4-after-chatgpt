import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Prints the current state of the board."""
    # Print column letters
    column_labels = "  ".join(chr(i) for i in range(ord('A'), ord('A') + len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")

    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")


def is_valid_column(column, board):
    """Checks if the input column is valid and has space available."""
    if not column.isalpha() or len(column) != 1:
        return False
    col_idx = ord(column.upper()) - ord('A')
    if col_idx < 0 or col_idx >= len(board[0]):
        return False
    return board[0][col_idx] == " "


def drop_checker(board, column, checker):
    """Drops the checker into the selected column."""
    col_idx = ord(column.upper()) - ord('A')
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx


def check_win(board, checker, row, col):
    """Checks if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check in both directions
        for sign in [-1, 1]:
            r, c = row, col
            while True:
                r += sign * dr
                c += sign * dc
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False


def is_draw(board):
    """Checks if the board is full and the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))


def main():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    clear_screen()
    print_board(board)

    players = CHECKERS
    current_player = random.randint(0, len(players) - 1)

    while True:
        print(f"Player {players[current_player]}, it's your turn!")
        column = input("Please enter a column letter: ").strip().upper()

        # Validate input
        if is_valid_column(column, board):
            row, col = drop_checker(board, column, players[current_player])
            clear_screen()
            print_board(board)

            # Check for a win
            if check_win(board, players[current_player], row, col):
                print(f"Player {players[current_player]} won!")
                break

            # Check for a draw
            if is_draw(board):
                print("It's a draw!")
                break

            # Switch to the next player
            current_player = (current_player + 1) % len(players)
        else:
            print("Invalid column, please try again!")


if __name__ == "__main__":
    main()
