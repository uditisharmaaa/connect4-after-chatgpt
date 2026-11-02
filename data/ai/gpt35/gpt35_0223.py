import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players, use first NUM_PLAYERS
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    line = "+" + "---+" * cols
    print(header)
    print(line)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(line)

def is_valid_column(col_letter, cols):
    return col_letter in string.ascii_uppercase[:cols]

def get_column_index(col_letter):
    return string.ascii_uppercase.index(col_letter)

def column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker at the lowest empty spot in column col_idx
    for r in range(len(board)-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    # Column full
    return None

def check_win(board, player_checker, r, c):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == player_checker:
            count += 1
            rr += dr
            cc += dc

        # Check in the negative direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == player_checker:
            count += 1
            rr -= dr
            cc -= dc

        if count >= WIN_COUNT:
            return True

    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def get_valid_input(board, cols):
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print("Invalid input, please enter a single column letter:")
            continue
        if not is_valid_column(user_input, cols):
            print("Invalid column, please enter a letter from A to {}:".format(string.ascii_uppercase[cols-1]))
            continue
        col_idx = get_column_index(user_input)
        if column_full(board, col_idx):
            print("Column full, turn lost.")
            return None
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)
    checker = players[current_player_idx]

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {checker}, please enter a column:")

        col_idx = get_valid_input(board, COLUMNS)
        if col_idx is None:
            # Turn lost, next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            checker = players[current_player_idx]
            continue

        placed = place_checker(board, col_idx, checker)
        if placed is None:
            # Should never happen due to validation before
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            checker = players[current_player_idx]
            continue

        r, c = placed
        if check_win(board, checker, r, c):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        checker = players[current_player_idx]

if __name__ == "__main__":
    main()
