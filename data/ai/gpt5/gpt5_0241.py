import os
import random
import sys

# Constants (you can change these for testing; final submission uses 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Top border
    print("+" + "---+" * cols)

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)


def get_column_input(max_cols):
    # Valid inputs are single uppercase letters from A to corresponding last letter
    last_letter = chr(ord('A') + max_cols - 1)
    prompt = f"Please enter a column (A-{last_letter}): "
    while True:
        try:
            user_in = input().strip()
        except (EOFError, KeyboardInterrupt):
            # Graceful exit on unexpected end
            print("\nExiting game.")
            sys.exit(0)

        if len(user_in) != 1:
            print(prompt, end="")
            continue

        ch = user_in
        if 'A' <= ch <= last_letter:
            return ord(ch) - ord('A')

        # Invalid input; ask again (turn is not lost)
        print(prompt, end="")


def place_checker(board, col, checker):
    # Place from bottom-most empty slot in the column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # Column full


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, down-left
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Basic validations for constants
    cols_ok = 1 <= COLS <= 26
    players_ok = 2 <= NUM_PLAYERS <= 5
    if not cols_ok or not players_ok:
        print("Configuration error: COLS must be 1..26 and NUM_PLAYERS must be 2..5.")
        return

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current]}, please enter a column:")

        col = get_column_input(COLS)

        row = place_checker(board, col, players[current])
        if row == -1:
            # Column is full; turn lost
            # Proceed to next player
            current = (current + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, players[current]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current]} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
