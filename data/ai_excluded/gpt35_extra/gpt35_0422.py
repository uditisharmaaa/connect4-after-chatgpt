import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COL_LABELS))
    # Print board rows
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        line = "|"
        for col in range(COLS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * COLS)

def valid_column_input(input_str):
    if len(input_str) != 1:
        return False
    if input_str not in COL_LABELS:
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter) - ord('A')

def column_is_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in the lowest empty slot in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # If column is full, return None
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all directions for win (need 4 in a row)
    # Directions: horizontal, vertical, diagonal up-right, diagonal down-right
    directions = [
        ((0, -1), (0, 1)),   # horizontal left and right
        ((-1, 0), (1, 0)),   # vertical up and down
        ((-1, -1), (1, 1)),  # diagonal up-left and down-right
        ((-1, 1), (1, -1))   # diagonal up-right and down-left
    ]
    for dir1, dir2 in directions:
        count = 1  # Current checker counts as 1
        count += check_direction(board, row + dir1[0], col + dir1[1], dir1[0], dir1[1], checker)
        count += check_direction(board, row + dir2[0], col + dir2[1], dir2[0], dir2[1], checker)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if not column_is_full(board, col):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")
        player_input = input().strip().upper()

        if not valid_column_input(player_input):
            # Invalid input (not single letter or out of bounds)
            continue
        
        col_index = get_column_index(player_input)
        if column_is_full(board, col_index):
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        placed = place_checker(board, col_index, checker)
        if placed is None:
            # Should not happen because of column_is_full check but safe guard
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        row_placed, col_placed = placed

        print_board(board)

        # Check for win
        if check_win(board, row_placed, col_placed, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
