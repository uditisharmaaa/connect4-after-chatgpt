import os
import random
import sys

# Configuration constants
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Header
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+---" * cols + "+")
    for r in range(rows):
        print("| " + " | ".join(board[r]) + " |")
        print("+---" * cols + "+")


def get_valid_column_input(cols, checker):
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        ch = user_input.upper()
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Please enter a letter A-Z.")
            continue
        col = ord(ch) - ord('A')
        if not (0 <= col < cols):
            print("Invalid column. Please choose a column within the board.")
            continue
        return col


def place_checker(board, col, checker):
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def validate_configuration():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return False
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return False
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return False
    return True


def main():
    if not validate_configuration():
        sys.exit(1)

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        checker = players[current_player_idx]
        # Show updated board at the start of the turn
        clear_screen()
        print_board(board)

        col = get_valid_column_input(COLS, checker)
        placed_row = place_checker(board, col, checker)

        if placed_row is None:
            # Column full, turn lost
            print(f"Column {chr(ord('A') + col)} is full. Player {checker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, check for win or draw
        if check_winner(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
