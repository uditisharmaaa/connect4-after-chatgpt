import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    # Print top border
    sep = "+---" * len(board[0]) + "+"
    for row in range(len(board)):
        print(sep)
        print("| " + " | ".join(board[row]) + " |")
    print(sep)

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if not ('A' <= col_letter <= chr(ord('A') + cols - 1)):
        return False
    return True

def column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col_idx, checker):
    # Piece falls to lowest empty row in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Column full
    return None, None

def check_winner(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal \, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Check forward direction
        rr, cc = row + dr, col + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc

        # Check backward direction
        rr, cc = row - dr, col - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc

        if count >= WIN_LENGTH:
            return True

    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS_CHECKERS[:NUM_PLAYERS]

    # Random start player
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        col_input = input(prompt).strip().upper()

        if not is_valid_column(col_input, COLUMNS):
            # Invalid input do not change turn
            continue

        col_idx = column_index(col_input)
        row_idx, col_idx = place_checker(board, col_idx, current_checker)

        if row_idx is None:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check if current player won
        if check_winner(board, row_idx, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
