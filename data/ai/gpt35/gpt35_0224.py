import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    line = "+---" * len(board[0]) + "+"
    for row in range(len(board)):
        print(line)
        print("| " + " | ".join(board[row]) + " |")
    print(line)

def is_valid_column(column_char, board):
    if len(column_char) != 1:
        return False
    upper = column_char.upper()
    if upper < 'A' or upper >= chr(ord('A') + len(board[0])):
        return False
    col_idx = ord(upper) - ord('A')
    # Check if column is full
    return board[0][col_idx] == " "

def get_column_index(column_char, board):
    return ord(column_char.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Places a checker in the given column; 
    returns row index where placed, or None if full
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return None

def check_win(board, row, col, checker):
    max_r, max_c = len(board), len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < max_r and 0 <= c < max_c and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Check all directions; win if total count (both sides + 1) >= WIN_COUNT
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # current checker
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def next_player_index(current_idx):
    return (current_idx + 1) % PLAYERS

def input_column(current_player, board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").strip()
        if not is_valid_column(col, board):
            if len(col) == 1 and col.upper() >= 'A' and col.upper() < chr(ord('A') + len(board[0])):
                # Column is valid character but full, lose turn
                col_idx = get_column_index(col, board)
                if board[0][col_idx] != " ":
                    # According to spec: "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
                    return None
            print("Invalid input. Please enter a valid column letter corresponding to a non-full column.")
            continue
        return col

def main():
    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:PLAYERS]

    # Random first player
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = checkers[current_player_idx]
        player_name = current_checker

        col_char = input_column(current_checker, board)
        # If col_char is None, column is full - lose turn
        if col_char is None:
            current_player_idx = next_player_index(current_player_idx)
            print_board(board)
            continue

        col_idx = get_column_index(col_char, board)
        # Place checker in board
        row = place_checker(board, col_idx, current_checker)
        print_board(board)

        if row is None:
            # Should not happen here because we validate above
            current_player_idx = next_player_index(current_player_idx)
            continue

        if check_win(board, row, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = next_player_index(current_player_idx)

if __name__ == "__main__":
    main()
