import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set number of players here (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C...)
    header = "  "
    for i in range(COLUMNS):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print rows with separators
    line = "+---" * COLUMNS + "+"
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)

def valid_column_input(col_input):
    if len(col_input) != 1:
        return False
    if not ('A' <= col_input <= chr(ord('A') + COLUMNS - 1)):
        return False
    return True

def column_index(col_input):
    return ord(col_input) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in lowest available row in column col_idx
    # Returns True if placed successfully, False if column full
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # Vertical check
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # Diagonal "\" check (down-right)
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal "/" check (up-right)
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def main():
    if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return

    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = column_index(user_input)
            # Try to place checker, if column full, lose turn and break input loop
            if not place_checker(board, col, current_checker):
                print("Column is full. You lose your turn.")
                break
            else:
                # Successfully placed checker
                break

        # After placing or losing turn, check win or draw
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
