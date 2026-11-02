import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print board with row separators
    for row in board:
        print("+" + "---+" * cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * cols)

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    col = input_str[0]
    if col not in string.ascii_uppercase[:cols]:
        return False
    return True

def drop_checker(board, col_idx, checker):
    # Place checker in lowest available row in col_idx
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Column full

def check_win(board, checker, last_row, last_col):
    rows = len(board)
    cols = len(board[0])

    def count_consecutive(r_step, c_step):
        count = 1  # Include the last placed checker itself

        # Check in the positive direction
        r, c = last_row + r_step, last_col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step

        # Check in the negative direction
        r, c = last_row - r_step, last_col - c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= r_step
            c -= c_step

        return count

    # Directions to check: horizontal, vertical, diagonal /
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        if count_consecutive(dr, dc) >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    rows = ROWS
    cols = COLS
    num_players = 2
    players = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        prompt = f"Player {player_checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, cols):
                continue  # Invalid input, ask again

            col_idx = ord(user_input) - ord('A')
            placed_pos = drop_checker(board, col_idx, player_checker)
            if placed_pos is None:
                # Column full, player loses the turn
                break
            else:
                break

        print_board(board)

        if placed_pos is not None:
            row_idx, col_idx = placed_pos
            if check_win(board, player_checker, row_idx, col_idx):
                print(f"Player {player_checker} won!")
                return
            if board_full(board):
                print("The game is a draw.")
                return

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
