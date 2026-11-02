import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Change this to 3, 4, or 5 for additional players
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_PLAYERS = len(CHECKERS)

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows if testing on Windows

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    col_labels = [chr(65 + i) for i in range(len(board[0]))]
    header = "  " + "   ".join(col_labels)
    separator = "+---" * len(board[0]) + "+"
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(column, board):
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < len(board[0]) and any(
        row[ord(column.upper()) - 65] == " " for row in board
    )

def get_next_open_row(column, board):
    col_idx = ord(column.upper()) - 65
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return -1

def place_checker(column, checker, board):
    row_idx = get_next_open_row(column, board)
    col_idx = ord(column.upper()) - 65
    board[row_idx][col_idx] = checker

def is_winner(board, rows, cols, player):
    # Horizontal check
    for row in range(rows):
        for col in range(cols - 3):
            if board[row][col] == player and all(
                board[row][col + i] == player for i in range(4)
            ):
                return True
    # Vertical check
    for row in range(rows - 3):
        for col in range(cols):
            if board[row][col] == player and all(
                board[row + i][col] == player for i in range(4)
            ):
                return True
    # Diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == player and all(
                board[row + i][col + i] == player for i in range(4)
            ):
                return True
    # Diagonal (down-left)
    for row in range(rows - 3):
        for col in range(3, cols):
            if board[row][col] == player and all(
                board[row + i][col - i] == player for i in range(4)
            ):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    # Game initialization
    if PLAYERS > MAX_PLAYERS:
        print(f"Maximum supported players: {MAX_PLAYERS}")
        return

    board = create_board(ROWS, COLUMNS)
    player_tokens = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        current_player = player_tokens[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip()

        if not is_valid_column(user_input, board):
            print("Invalid input. Please try again.")
            continue

        place_checker(user_input, current_player, board)
        clear_screen()
        print_board(board)

        # Check for win
        if is_winner(board, ROWS, COLUMNS, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
