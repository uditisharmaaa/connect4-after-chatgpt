import os
import random
import string

# Constants for the game setup
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4
PLAYERS = ["X", "O", "V", "H", "M"]  # Available checkers for players


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    """Creates a board filled with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Prints the current state of the board with column labels."""
    columns = len(board[0])
    header = "  "
    letters = string.ascii_uppercase
    for c in range(columns):
        header += f" {letters[c]}  "
    print(header)

    sep = "+" + "---+" * columns
    for row in board:
        print(sep)
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
    print(sep)


def choose_starting_player(num_players):
    """Randomly chooses the index of the starting player."""
    return random.randint(0, num_players - 1)


def input_column(current_player, columns):
    """Prompts the player to input a valid column letter."""
    letters = string.ascii_uppercase[:columns]
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(choice) != 1:
            print("Invalid input. Please enter exactly one letter.")
            continue
        if choice not in letters:
            print(f"Invalid column. Please choose a column between {letters[0]} and {letters[-1]}.")
            continue
        return letters.index(choice)


def place_checker(board, column, checker):
    """Places the checker in the specified column if possible.
       Returns True if placed, False if the column is full."""
    for row in reversed(range(len(board))):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False  # column full


def is_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal checks
    # \ diagonal
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # / diagonal
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False


def is_draw(board):
    """Returns True if the board is full (draw), False otherwise."""
    return all(cell != " " for row in board for cell in row)


def main():
    # Setup game with constants (6 rows x 7 columns and 2 players)
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS[:num_players]

    # Create board and choose starting player
    board = create_board(rows, columns)
    current_player_index = choose_starting_player(num_players)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]

        col = input_column(current_checker, columns)
        placed = place_checker(board, col, current_checker)

        if not placed:
            # Column full, player loses turn
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_checker} loses this turn.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % num_players
            continue

        # Check for win
        if is_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
