import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(labels))
    # Print rows with separators
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def is_valid_column(col_letter):
    if len(col_letter) != 1:
        return False
    col_letter = col_letter.upper()
    if ord(col_letter) < ord('A') or ord(col_letter) >= ord('A') + COLS:
        return False
    return True

def get_column_index(col_letter):
    return ord(col_letter.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in lowest empty row of col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full

def check_winner(board, row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLS):
        count = count + 1 if board[row][c] == checker else 0
        if count >= 4:
            return True

    # Check vertical
    count = 0
    for r in range(ROWS):
        count = count + 1 if board[r][col] == checker else 0
        if count >= 4:
            return True

    # Check diagonal /
    count = 0
    r_start = row
    c_start = col
    while r_start > 0 and c_start < COLS - 1:
        r_start -= 1
        c_start += 1
    r, c = r_start, c_start
    count = 0
    while r < ROWS and c >= 0:
        count = count + 1 if board[r][c] == checker else 0
        if count >= 4:
            return True
        r += 1
        c -= 1

    # Check diagonal \
    r_start = row
    c_start = col
    while r_start > 0 and c_start > 0:
        r_start -= 1
        c_start -= 1
    r, c = r_start, c_start
    count = 0
    while r < ROWS and c < COLS:
        count = count + 1 if board[r][c] == checker else 0
        if count >= 4:
            return True
        r += 1
        c += 1

    return False

def board_full(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        player_checker = players[current_player_index]
        print(f"Player {player_checker}, please enter a column:")

        col_input = input().strip().upper()
        if not is_valid_column(col_input):
            # Invalid input, ask again
            continue
        col = get_column_index(col_input)

        placed_row = place_checker(board, col, player_checker)
        if placed_row == -1:
            # Column full, lose turn
            # Just move to next player
            current_player_index = (current_player_index +1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, placed_row, col, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
