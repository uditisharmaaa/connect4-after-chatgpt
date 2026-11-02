import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    # Print board rows
    cols = len(board[0])
    row_sep = "+" + "---+" * cols
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)

def is_valid_column(column_letter, board):
    if not column_letter.isalpha() or len(column_letter) != 1:
        return False
    col_idx = ord(column_letter) - ord('A')
    if col_idx < 0 or col_idx >= len(board[0]):
        return False
    # If the top cell (row 0) is not empty, column is full
    if board[0][col_idx] != " ":
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter) - ord('A')

def place_checker(board, col_idx, checker):
    # Start from bottom row, find first empty cell
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Should never reach here if validity was checked before
    return None, None

def check_direction(board, start_row, start_col, dr, dc, checker):
    count = 0
    r, c = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_row, last_col, checker):
    # Directions: horizontal (0,1), vertical (1,0),
    # diagonal down-right (1,1), diagonal down-left (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # Count left/up from last checker
        count1 = check_direction(board, last_row, last_col, dr, dc, checker)
        # Count right/down minus 1 (to avoid double counting last checker)
        count2 = check_direction(board, last_row - dr, last_col - dc, -dr, -dc, checker)
        if count1 + count2 - 1 >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If any cell in top row is empty, board is not full
    return all(cell != " " for cell in board[0])

def get_player_input(player, board):
    while True:
        col_letter = input(f"Player {player}, please enter a column: ").strip().upper()
        if not is_valid_column(col_letter, board):
            # Special case: column full: player loses turn
            col_idx = ord(col_letter) - ord('A') if col_letter.isalpha() and len(col_letter) == 1 else None
            if col_idx is not None and 0 <= col_idx < len(board[0]) and board[0][col_idx] != " ":
                # Column full → lose turn
                return None
            print("Invalid input, please try again.")
            continue
        return col_letter

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly choose player index to start
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col_letter = get_player_input(current_checker, board)

        if col_letter is None:
            # Player loses turn if column full (top cell occupied)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        col_idx = get_column_index(col_letter)
        row_idx, col_idx = place_checker(board, col_idx, current_checker)
        print_board(board)

        if check_win(board, row_idx, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
