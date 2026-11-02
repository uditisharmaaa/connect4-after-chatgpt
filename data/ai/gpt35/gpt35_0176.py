import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to MAX_PLAYERS

# Use only 2 players for submission as requested
NUM_PLAYERS = 2
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    col_labels = string.ascii_uppercase[:cols]
    print("  " + "   ".join(col_labels))
    # Print separator line
    line_sep = "+" + "---+" * cols
    # Print rows
    for r in range(rows):
        print(line_sep)
        row_str = "|"
        for c in range(cols):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(line_sep)

def get_valid_column_input(board, player):
    cols = len(board[0])
    col_labels = string.ascii_uppercase[:cols]
    while True:
        user_input = input(f"Player {player}, please enter a column: ").upper()
        if len(user_input) != 1 or user_input not in col_labels:
            # Invalid input - not a single valid letter
            print(f"Invalid column. Please enter a letter between {col_labels[0]} and {col_labels[-1]}.")
            continue
        col_index = col_labels.index(user_input)
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full - player loses turn
            return None
        return col_index

def place_checker(board, col_index, player):
    # Place player's checker in the lowest empty space in the column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player
            return r, col_index
    return None  # Should never happen if checked column fullness before

def check_win(board, last_row, last_col, player):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = last_row, last_col
        # Count backwards
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        r, c = last_row + dr, last_col + dc
        # Count forwards
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count - 1  # last cell counted twice

    # Directions to check: horizontal, vertical, diagonal down-right, diagonal down-left
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        if count_direction(dr, dc) >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # If top row contains space, not draw
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = PLAYERS
    num_players = len(players)

    # Randomly select first player
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player = players[current_player_idx]
        col_index = get_valid_column_input(board, player)
        if col_index is None:
            # Column full - lose turn
            print(f"Column full. Player {player} loses turn.")
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue

        pos = place_checker(board, col_index, player)
        print_board(board)

        if check_win(board, pos[0], pos[1], player):
            print(f"Player {player} won!")
            break

        if check_draw(board):
            print("Game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
