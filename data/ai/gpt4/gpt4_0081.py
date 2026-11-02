import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"][:2]  # Adjust number of players here


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  " + "   ".join(letters[:len(board[0])]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")


def is_valid_column(col, board):
    return 0 <= col < len(board[0]) and board[0][col] == " "


def find_row_for_placement(column, board):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            return r
    return None


def check_win(board, player):
    # Check horizontal win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical win
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True

    return False


def check_draw(board):
    return all(board[0][c] != " " for c in range(len(board[0])))


def main():
    # Initialization
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    clear_screen()
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ", end="")
        column_input = input().strip().upper()

        # Validate input
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(column_input) - 65
        if not is_valid_column(column, board):
            print("Invalid column. Please choose a different column.")
            continue

        # Place the checker
        row = find_row_for_placement(column, board)
        board[row][column] = current_player

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)


if __name__ == "__main__":
    main()
