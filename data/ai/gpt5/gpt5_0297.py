import os
import random

# ----- Configuration (you may change these for testing) -----
ROWS = 6
COLS = 7   # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
# ------------------------------------------------------------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Print column headers A..Z
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))
    # Print top border
    print("+" + ("---+" * cols))
    # Print each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))

def drop_checker(board, col_idx, checker):
    rows = len(board)
    # Start from bottom row up
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False  # column full

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Horizontal
    for r in range(rows):
        for c in range(cols - needed + 1):
            if all(board[r][c + k] == checker for k in range(needed)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - needed + 1):
            if all(board[r + k][c] == checker for k in range(needed)):
                return True

    # Diagonal down-right
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r + k][c + k] == checker for k in range(needed)):
                return True

    # Diagonal up-right
    for r in range(needed - 1, rows):
        for c in range(cols - needed + 1):
            if all(board[r - k][c + k] == checker for k in range(needed)):
                return True

    return False

def get_valid_column_input(cols):
    while True:
        try:
            user_input = input("Please enter a column: ").strip()
        except EOFError:
            # Treat EOF as invalid; keep asking
            continue
        except KeyboardInterrupt:
            # Treat Ctrl-C as invalid; keep asking
            print()
            continue

        if len(user_input) != 1:
            print("Invalid input. Enter a single letter for the column.")
            continue

        ch = user_input.upper()
        if not ('A' <= ch <= 'Z'):
            print("Invalid character. Enter a letter A-Z.")
            continue

        col_idx = ord(ch) - ord('A')
        if col_idx < 0 or col_idx >= cols:
            print("Column out of range.")
            continue

        return col_idx

def main():
    # Clamp settings to allowed ranges
    cols = max(1, min(COLS, 26))
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))
    player_checkers = CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly select starting player
    current_player = random.randrange(num_players)

    # Initial screen
    clear_screen()
    print_board(board)
    print(f"Player {player_checkers[current_player]}, please enter a column:")

    while True:
        # Ask current player for a move (validated)
        col_idx = get_valid_column_input(cols)

        # Try to drop the checker
        placed = drop_checker(board, col_idx, player_checkers[current_player])

        # Clear and print updated board
        clear_screen()
        print_board(board)

        if not placed:
            # Column full -> lose the turn
            print(f"Column {chr(ord('A') + col_idx)} is full. Player {player_checkers[current_player]} loses the turn.")
            # Next player
            current_player = (current_player + 1) % num_players
        else:
            # Check for win
            if check_win(board, player_checkers[current_player]):
                print(f"Player {player_checkers[current_player]} won!")
                break

            # Check for draw
            if board_full(board):
                print("The game is a draw.")
                break

            # Next player
            current_player = (current_player + 1) % num_players

        # Prompt next player
        print(f"Player {player_checkers[current_player]}, please enter a column:")

if __name__ == "__main__":
    main()
