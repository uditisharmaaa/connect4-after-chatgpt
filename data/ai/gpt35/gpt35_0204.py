import os
import random

# Constants (set as requested in submission section)
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows with separators
    for row in range(len(board)):
        print("+" + "---+" * len(board[0]))
        print("|" + "|".join(f" {board[row][col]} " for col in range(len(board[0]))) + "|")
    print("+" + "---+" * len(board[0]))

def valid_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input not in COLUMN_LABELS:
        return False
    return True

def column_full(board, col_idx):
    # If top row of column is not empty, full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker at lowest empty spot in column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Column full

def check_win(board, checker, last_row, last_col):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 1  # count the last placed checker itself
        # check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count

    # directions: horizontal, vertical, diagonal /
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        if count_direction(dr, dc) >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If top row has any empty space, not full
    return all(cell != " " for cell in board[0])

def get_player_input(player_checker):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not valid_input(user_input):
            continue
        col_idx = COLUMN_LABELS.index(user_input)
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]

        col_idx = get_player_input(checker)
        if column_full(board, col_idx):
            # lose turn if column full
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue
        last_pos = place_checker(board, col_idx, checker)
        print_board(board)

        if check_win(board, checker, last_pos[0], last_pos[1]):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            # board filled and no winner
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
