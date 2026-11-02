import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    print("  " + "   ".join(chr(ord('A') + i) for i in range(cols)))
    for row in range(len(board)):
        print("+" + "---+" * cols)
        print("| " + " | ".join(board[row]) + " |")
    print("+" + "---+" * cols)

def valid_column_input(inp, board):
    if len(inp) != 1:
        return False
    ch = inp[0]
    if not ('A' <= ch <= chr(ord('A') + len(board[0]) - 1)):
        return False
    col = ord(ch) - ord('A')
    # Check if column is full
    if board[0][col] != " ":
        return False
    return True

def get_next_open_row(board, col):
    # start from bottom row up to find empty spot
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            return r
    return -1  # no open row

def place_checker(board, col, checker):
    row = get_next_open_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal "/" direction (bottom-left to top-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal "\" direction (top-left to bottom-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def is_board_full(board):
    # If top row has any empty space, board is not full
    return all(cell != " " for cell in board[0])

def main():
    # Setup game settings
    rows = 6
    cols = 7
    num_players = 2
    checkers = PLAYERS[:num_players]

    board = create_board(rows, cols)

    current_player_idx = random.randint(0, num_players - 1)
    while True:
        print_board(board)
        current_checker = checkers[current_player_idx]
        inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        while not valid_column_input(inp, board):
            # Either invalid letter or column full on top
            if len(inp) != 1 or not ('A' <= inp <= chr(ord('A') + cols - 1)):
                print("Invalid input. Please enter a valid column letter (e.g. A, B, C...).")
            else:
                # Check if column full
                col = ord(inp) - ord('A')
                if board[0][col] != " ":
                    print("That column is completely filled. Turn lost.")
                    break
            inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        # If invalid input caused turn lost, skip placing checker and move on
        if len(inp) == 1 and ('A' <= inp <= chr(ord('A') + cols - 1)):
            col = ord(inp) - ord('A')
            placed = place_checker(board, col, current_checker)
            if not placed:
                # Column full - skip turn
                current_player_idx = (current_player_idx + 1) % num_players
                continue

            if check_winner(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            if is_board_full(board):
                print_board(board)
                print("Game is a draw!")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
