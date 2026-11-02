import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    # Top border
    print("+---" * cols + "+")
    # Rows
    for r in range(len(board)):
        row = board[r]
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")


def get_players(n):
    n = max(2, min(5, n))
    return CHECKERS[:n]


def column_from_input(user_inp, cols):
    user_inp = user_inp.strip().upper()
    if len(user_inp) != 1:
        return None
    if user_inp < "A" or user_inp > "Z":
        return None
    idx = ord(user_inp) - ord("A")
    if idx < 0 or idx >= cols:
        return None
    return idx


def find_drop_row(board, col):
    # Return the row index where the checker will land, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def check_winner(board):
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            if ch == " ":
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc) and board[rr][cc] == ch:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return ch
    return None


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Setup
    cols = max(1, min(26, COLS))
    rows = max(1, ROWS)
    players = get_players(NUM_PLAYERS)
    board = make_board(rows, cols)

    # Random first player
    current = random.randint(0, len(players) - 1)

    # Initial board print
    print_board(board)

    # Game loop
    while True:
        player = players[current]
        # Prompt for input until a valid column letter is given
        while True:
            user_inp = input(f"Player {player}, please enter a column: ")
            col = column_from_input(user_inp, cols)
            if col is None:
                # Invalid input, ask again (turn is not lost)
                print_board(board)
                print("Invalid input. Please enter a valid column letter.")
                continue
            else:
                break

        # Try to place checker
        row_to_place = find_drop_row(board, col)
        if row_to_place is None:
            # Column full, turn is lost
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {player} loses the turn.")
            current = (current + 1) % len(players)
            continue
        else:
            board[row_to_place][col] = player

        # Print board after move
        print_board(board)

        # Check for winner
        winner = check_winner(board)
        if winner is not None:
            print(f"Player {winner} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % len(players)


if __name__ == "__main__":
    main()
