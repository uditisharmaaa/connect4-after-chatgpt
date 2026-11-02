import os
import random
import sys

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print rows
    col_count = len(board[0])
    line = "+---" * col_count + "+"
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)

def input_column(player_checker, board):
    valid_cols = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        col_str = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(col_str) != 1 or col_str.upper() not in valid_cols:
            # Invalid input (wrong length or not in columns)
            continue
        col_index = ord(col_str.upper()) - ord('A')
        if board[0][col_index] != " ":
            # Column full: turn lost
            return None
        return col_index

def place_checker(board, col_index, player_checker):
    # Start from bottom row go upwards to find first free slot
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return row, col_index
    # If no space found, this shouldn't happen because we check before
    return None

def check_win(board, row, col, player_checker):
    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        return count

    # Check 4 directions (horizontal, vertical, two diagonals)
    directions = [
        ((0, 1), (0, -1)),  # horizontal (right, left)
        ((1, 0), (-1, 0)),  # vertical (down, up)
        ((1, 1), (-1, -1)), # diagonal down-right and up-left
        ((1, -1), (-1, 1)), # diagonal down-left and up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # count the placed checker itself
        count += count_direction(*dir1)
        count += count_direction(*dir2)
        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    # If any top cell is free, board is not full
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    if PLAYERS < 2 or PLAYERS > 5:
        print("Invalid number of players (must be between 2 and 5).")
        sys.exit(1)
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randrange(PLAYERS)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col_index = input_column(player_checker, board)
        if col_index is None:
            # Turn lost due to full column
            # Move to next player without placing checker
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        placed = place_checker(board, col_index, player_checker)
        print_board(board)
        r, c = placed

        if check_win(board, r, c, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("Game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
