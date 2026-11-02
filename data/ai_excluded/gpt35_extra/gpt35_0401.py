import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players
WIN_COUNT = 4


def clear_screen():
    os.system('clear')


def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    clear_screen()
    # Print column headers (A-G)
    headers = "  "
    for i in range(COLS):
        headers += chr(ord('A') + i) + "   "
    print(headers)
    # Print the board rows
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)


def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + COLS - 1):
        return True
    return False


def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')


def place_checker(board, col, checker):
    # Place checker in lowest empty spot in col, return True if placed, False if col full
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full


def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal (down-right) check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal (up-right) check
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False


def check_draw(board):
    # If no empty spaces any more, it's a draw
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {players[current_player_idx]}, please enter a column:")

        # Input loop until valid
        while True:
            col_input = input().strip()
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_idx = get_column_index(col_input)
            # Check if column full
            if board[0][col_idx] != " ":
                # Lose turn if full
                print("Column is full. You lose your turn.")
                break
            else:
                placed = place_checker(board, col_idx, players[current_player_idx])
                if placed:
                    break
                else:
                    # Should not get here because we check top cell first, but just in case
                    print("Column is full. You lose your turn.")
                    break

        # If checker placed (valid move), check win and draw
        if board[0][col_idx] == players[current_player_idx]:
            if check_win(board, players[current_player_idx]):
                print_board(board)
                print(f"Player {players[current_player_idx]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
