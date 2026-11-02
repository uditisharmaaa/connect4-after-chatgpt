import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Player checkers in order
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print the board rows
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for col in range(COLS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def valid_column_input(col_input):
    if len(col_input) != 1:
        return False
    if col_input not in COLUMN_LABELS:
        return False
    return True

def column_index(col_letter):
    return ord(col_letter) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # place checker in the lowest available row in given col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # return position where checker was placed
    return None  # column full

def check_win(board, row, col, checker):
    # Check horizontally, vertically, and both diagonals for WIN_COUNT
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count includes the last placed checker
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = players[current_player_index]
        prompt = f"Player {player_checker}, please enter a column: "

        valid_input = False
        while not valid_input:
            col_input = input(prompt).strip().upper()
            if not valid_column_input(col_input):
                continue
            col = column_index(col_input)
            if is_column_full(board, col):
                # Lose the turn if full, do not ask again
                valid_input = True
                placed = None
                break
            else:
                placed = place_checker(board, col, player_checker)
                valid_input = True

        print_board(board)

        if placed is None:
            # Column full and player loses turn
            # Just continue to next player
            pass
        else:
            row_placed, col_placed = placed
            if check_win(board, row_placed, col_placed, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_full(board):
                print("Game is a draw!")
                break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
