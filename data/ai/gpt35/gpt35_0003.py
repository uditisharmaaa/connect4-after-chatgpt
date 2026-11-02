import os
import random

# Constants - board dimensions and player checkers
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
NUM_PLAYERS = 2  # For submission, set to 2 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print horizontal separator line
    separator = "+" + "---+" * len(board[0])
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column_input(col_input, cols):
    if len(col_input) != 1:
        return False
    if not ('A' <= col_input <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_next_open_row(board, col):
    # Returns the lowest empty row index in the column, or None if full
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, checker):
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + offset] == checker for offset in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + offset][c] == checker for offset in range(WIN_COUNT)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(WIN_COUNT)):
                return True

    # Diagonal (down-left) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, cols):
            if all(board[r + offset][c - offset] == checker for offset in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def next_player_index(current_index, num_players):
    return (current_index + 1) % num_players

def main():
    # Prepare game variables
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]

    # Randomly pick starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        while True:
            col_input = input(prompt).strip().upper()
            if not is_valid_column_input(col_input, COLS):
                # Invalid input: not a single uppercase letter in range
                continue
            col_idx = ord(col_input) - ord('A')
            if board[0][col_idx] != " ":
                # Column full, player loses turn
                break
            else:
                # Place checker
                placed = place_checker(board, col_idx, current_checker)
                if placed:
                    break
                else:
                    # Should not reach here: means column full
                    break

        print_board(board)

        # If player placed their checker, check win and draw
        # If player lost turn (column full), skip win check and jump to next
        if board[0][col_idx] == current_checker:
            # Check win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check draw
            if board_full(board):
                print("The game is a draw.")
                break

        # Next player turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
