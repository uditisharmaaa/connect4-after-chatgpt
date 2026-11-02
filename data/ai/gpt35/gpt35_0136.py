import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players, use first PLAYERS elements
WIN_COUNT = 4
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()

    # Print column headers
    print("  " + "   ".join(COLUMN_LETTERS))
    # Print rows with separators
    for row in range(ROWS):
        print("+---" * COLS + "+")
        line = "|"
        for col in range(COLS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+---" * COLS + "+")

def is_valid_column(col_letter):
    return col_letter in COLUMN_LETTERS

def column_index(col_letter):
    return ord(col_letter) - ord('A')

def column_full(board, col_idx):
    # If top row (row 0) is occupied, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty row in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Column full
    return None

def check_win(board, last_row, last_col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diagonal down-right
        (1,-1), # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
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

        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If any spot in top row is empty, board is not full
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_idx]} starts.")

    while True:
        checker = players[current_player_idx]
        move_valid = False

        while not move_valid:
            print(f"Player {checker}, please enter a column:")
            user_input = input().strip().upper()

            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter.")
                continue
            if not is_valid_column(user_input):
                print("Invalid column letter. Please enter a valid column (A-G).")
                continue
            col_idx = column_index(user_input)
            if column_full(board, col_idx):
                # Player loses turn according to assignment
                print(f"Column {user_input} is full. You lose your turn.")
                move_valid = True
                placed_pos = None
                break
            placed_pos = place_checker(board, col_idx, checker)
            if placed_pos is not None:
                move_valid = True
            else:
                print("Unexpected error placing checker. Try again.")

        print_board(board)

        # Check win only if checker placed
        if placed_pos is not None:
            row, col = placed_pos
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
