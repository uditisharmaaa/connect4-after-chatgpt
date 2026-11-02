import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels (A, B, C, ...)
    labels = "  " + "   ".join(chr(ord("A")+i) for i in range(len(board[0])))
    print(labels)
    # Print the board with lines
    line = "+" + "---+" * len(board[0])
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def valid_column_input(user_input, board_columns):
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if not ('A' <= c <= chr(ord('A') + board_columns - 1)):
        return False
    return True

def get_column_index(user_input):
    return ord(user_input.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # start from bottom row (ROWS-1) go up
    for r in range(len(board)-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    return None  # column full

def check_win(board, row, col, checker):
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        prompt = f"Player {player_checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip()
            if not valid_column_input(user_input, COLUMNS):
                # invalid input, ask again (no turn lost)
                continue
            col = get_column_index(user_input)
            pos = place_checker(board, col, player_checker)
            if pos is None:
                # column full, turn lost
                break
            else:
                # valid move placed
                break

        print_board(board)

        if pos is not None:
            r, c = pos
            if check_win(board, r, c, player_checker):
                print(f"Player {player_checker} won!")
                break

        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
