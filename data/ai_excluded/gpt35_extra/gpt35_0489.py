import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print("+" + "---+" * COLUMNS)

def is_valid_column(col_char):
    if col_char in COLUMN_LABELS:
        return True
    return False

def column_index(col_char):
    return ord(col_char) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place the checker in the lowest free row in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row  # Return the row where checker placed
    return -1  # If column full

def check_winner(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    # If top row has no empty spaces, board is full
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS_COUNT]
    current_player_index = random.randint(0, PLAYERS_COUNT -1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col_char = ""
        while True:
            print(f"Player {current_checker}, please enter a column:")
            col_char = input().strip().upper()
            if not is_valid_column(col_char):
                continue
            col = column_index(col_char)
            if is_column_full(board, col):
                # Turn is lost if column full
                print("Column full. You lose your turn.")
                break
            else:
                row_placed = place_checker(board, col, current_checker)
                if row_placed != -1:
                    break

        print_board(board)

        # Check for win only if checker was placed
        if col_char != "" and not is_column_full(board, column_index(col_char)):
            if check_winner(board, row_placed, col, current_checker):
                print(f"Player {current_checker} won!")
                break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
