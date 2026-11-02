import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # supported checkers for up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    sep_line = "+" + "---+" * len(board[0])
    for row in board:
        print(sep_line)
        print("| " + " | ".join(row) + " |")
    print(sep_line)

def get_valid_column_input(board):
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + cols - 1)}:")
            continue
        if user_input not in valid_cols:
            print(f"Invalid input. Please enter a column letter from A to {chr(ord('A') + cols - 1)}:")
            continue
        col_index = ord(user_input) - ord('A')
        # Check if the column is full
        if board[0][col_index] != " ":
            # According to spec: If column full, turn invalid, player loses turn
            return col_index, False
        return col_index, True

def place_checker(board, col, checker):
    """
    Place the checker in the given column in the lowest empty slot.
    Assumes the column is not full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # shouldn't happen if checked before

def check_win(board, checker, last_row, last_col):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal (0,1), vertical (1,0), diag1 (1,1), diag2 (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # Count checkers of the same type in positive and negative directions
        total = 1 + count_direction(dr, dc) + count_direction(-dr, -dc)
        if total >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If top row has no spaces, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")

        col_index, valid_turn = get_valid_column_input(board)
        if not valid_turn:
            # According to spec, turn lost if column full, so no placing checker
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        row_index, _ = place_checker(board, col_index, checker)
        print_board(board)

        # Check for win
        if check_win(board, checker, row_index, col_index):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
