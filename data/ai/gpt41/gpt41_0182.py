import os
import random

# Constants -- Change these to support more players/different board sizes
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Derived constants
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    # Works for Unix-based systems
    os.system('clear')


def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Print separator
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)


def get_valid_column_input(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()

        # Input must be a single character, an alphabet, and within current columns
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column label.")
            continue

        col = COLUMN_LABELS.index(col_input)

        # Check if column is full
        if board[0][col] != " ":
            print("This column is full. You lose your turn.")
            return None  # Loss of turn
        return col


def drop_checker(board, col, checker):
    # Place the checker in the lowest available space in the specified column
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return board.index(row), col  # Returns position (row, col)


def check_win(board, row, col, checker):
    # Directions: [(dy, dx)]
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]

    for dy, dx in directions:
        count = 1  # Count the placed checker

        # Check one direction
        r, c = row + dy, col + dx
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dy
            c += dx

        # Check opposite direction
        r, c = row - dy, col - dx
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dy
            c -= dx

        if count >= 4:
            return True
    return False


def board_full(board):
    # If the top row has no " ", the whole board is full
    return all(cell != " " for cell in board[0])


def main():
    board = create_board()

    # For this assignment, only use up to PLAYERS checkers and players
    player_checkers = CHECKERS[:PLAYERS]
    player_names = player_checkers

    # Pick a random player to start
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {player_names[current_player_index]} will start!")

    game_over = False

    while not game_over:
        checker = player_checkers[current_player_index]
        print_board(board)
        col = get_valid_column_input(board, checker)

        # If turn lost, skip to next player
        if col is None:
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        row, col = drop_checker(board, col, checker)
        print_board(board)

        # Check win after move
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
            continue

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Move to next player
        current_player_index = (current_player_index + 1) % PLAYERS


# Run if executed directly
if __name__ == "__main__":
    main()
