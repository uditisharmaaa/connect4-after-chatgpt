import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 for more players (max 5)
CONNECT_N = 4    # Number of checkers in-line needed to win
MAX_COLUMNS = 26 # Limit for column labels (A-Z)

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, col_labels):
    print()
    print("  " + "   ".join(col_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_columns(board):
    return [i for i in range(len(board[0])) if board[0][i] == " "]

def get_input(col_labels, valid_cols):
    while True:
        choice = input().strip().upper()
        if len(choice) != 1 or choice not in col_labels:
            print("Invalid input. Please enter a valid column letter:")
            continue
        col = col_labels.index(choice)
        if col not in valid_cols:
            print("Column is full. You lose your turn.")
            return None # Lose turn if column full (as per assignment)
        return col

def place_checker(board, col, checker):
    # Place from bottommost available row in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None

def check_win(board, row, col, checker):
    # Returns True if the last move at (row, col) caused a win
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # main diagonal
        (1, -1)  # anti-diagonal
    ]
    for dr, dc in directions:
        count = 1
        # check both forward and backward in this direction
        for sign in (-1, 1):
            r, c = row, col
            while True:
                r += dr * sign
                c += dc * sign
                if 0 <= r < len(board) and 0 <= c < len(board[0]):
                    if board[r][c] == checker:
                        count += 1
                    else:
                        break
                else:
                    break
        if count >= CONNECT_N:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    rows = ROWS
    cols = COLUMNS
    num_players = NUM_PLAYERS
    checkers = PLAYER_CHECKERS[:num_players]
    col_labels = list(string.ascii_uppercase[:cols])
    board = create_board(rows, cols)
    current_player = random.randint(0, num_players - 1)
    clear_screen()
    print_board(board, col_labels)
    print(f"Player {checkers[current_player]}, please enter a column:")
    turn_count = 0

    while True:
        valid_cols = get_valid_columns(board)
        if len(valid_cols) == 0:
            print("The board is full. It's a draw!")
            break

        col = get_input(col_labels, valid_cols)
        if col is None:
            # Player loses their turn due to choosing full column
            current_player = (current_player + 1) % num_players
            clear_screen()
            print_board(board, col_labels)
            print(f"Player {checkers[current_player]}, please enter a column:")
            continue

        row, c = place_checker(board, col, checkers[current_player])

        clear_screen()
        print_board(board, col_labels)

        if check_win(board, row, col, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        elif board_full(board):
            print("The board is full. It's a draw!")
            break

        current_player = (current_player + 1) % num_players
        print(f"Player {checkers[current_player]}, please enter a column:")

if __name__ == "__main__":
    main()
