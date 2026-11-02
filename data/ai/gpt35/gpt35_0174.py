import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(headers))
    # Print the board rows with separators
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def column_index(col_char):
    col_char = col_char.upper()
    if len(col_char) == 1 and 'A' <= col_char <= chr(ord('A') + COLS - 1):
        return ord(col_char) - ord('A')
    return -1

def get_player_input(player, board):
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        col = column_index(choice)
        if col == -1:
            print("Invalid input. Please enter a valid column letter (A to {}).".format(chr(ord('A') + COLS -1)))
            continue
        # Check if column is full
        if board[0][col] != " ":
            # According to assignment: player loses turn if column full
            return -1
        return col

def place_checker(board, col, checker):
    # Start from bottom row to top to find first empty space
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should never reach here because we check full column before
    return -1, -1

def check_winner(board, checker, last_row, last_col):
    # Directions: horizontal, vertical, diagonal (2 directions)
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count the last placed checker itself
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col = get_player_input(current_checker, board)

        if col == -1:
            # Column full, player loses turn
            current_player_index = (current_player_index +1) % PLAYERS
            continue

        row, placed_col = place_checker(board, col, current_checker)
        print_board(board)

        if check_winner(board, current_checker, row, placed_col):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index +1) % PLAYERS

if __name__ == "__main__":
    main()
