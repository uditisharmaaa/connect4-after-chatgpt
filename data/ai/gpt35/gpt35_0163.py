import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]  # Only use first NUM_PLAYERS checkers

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(header)
    # Print the top border
    print("+" + "---+" * len(board[0]))
    # Print the rows
    for row in board:
        line = "| " + " | ".join(row) + " |"
        print(line)
        print("+" + "---+" * len(board[0]))

def get_valid_column_input(board, player_checker):
    valid_columns = string.ascii_uppercase[:len(board[0])]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate input length and character range
        if len(col_input) != 1 or col_input not in valid_columns:
            print(f"Invalid input. Please enter a single letter from {valid_columns}.")
            continue
        col_idx = valid_columns.index(col_input)
        # Check if the column is full
        if board[0][col_idx] != " ":
            # Column full -> turn lost, no re-input
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker on lowest available row in the column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Should never get here if checked before, but just in case
    return None, None

def check_winner(board, last_row, last_col, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # If top row has no empty spaces, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS_CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        col_idx = get_valid_column_input(board, current_checker)

        if col_idx is None:
            # Column full, player loses turn
            print(f"Column is full. Player {current_checker} loses the turn.")
            input("Press Enter to continue...")
            # Switch player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        last_row, last_col = place_checker(board, col_idx, current_checker)

        clear_screen()
        print_board(board)

        if check_winner(board, last_row, last_col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
