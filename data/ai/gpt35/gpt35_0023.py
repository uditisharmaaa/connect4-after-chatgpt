import os
import random

# Constants
ROWS = 6           # Number of rows in board
COLUMNS = 7        # Number of columns in board (max 26)
PLAYERS = 2        # Number of players (2 to 5)
WIN_LEN = 4        # Number of checkers in row to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Player checkers in order

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column headers (A, B, C ...)
    header = "  "
    for col in range(columns):
        header += f"  {chr(ord('A')+col)} "
    print(header)
    # Print separator line
    sep_line = "+" + "---+"*columns
    print(sep_line)
    for row in range(len(board)):
        line = "|"
        for col in range(columns):
            line += f" {board[row][col]} |"
        print(line)
        print(sep_line)

def valid_column_input(user_input, columns):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if 'A' <= ch < chr(ord('A') + columns):
        return True
    return False

def column_index_from_letter(letter):
    return ord(letter.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker at the lowest empty spot in the column
    # Return True if placed successfully, False if column full
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    columns = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(columns - WIN_LEN + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LEN)):
                return True
    # Vertical check
    for c in range(columns):
        for r in range(rows - WIN_LEN + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LEN)):
                return True
    # Diagonal (down-right)
    for r in range(rows - WIN_LEN + 1):
        for c in range(columns - WIN_LEN + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LEN)):
                return True
    # Diagonal (up-right)
    for r in range(WIN_LEN - 1, rows):
        for c in range(columns - WIN_LEN + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LEN)):
                return True
    return False

def check_draw(board):
    # Draw if no empty spaces left in any column
    return all(cell != " " for row in board for cell in row)

def get_next_player_index(current_index):
    return (current_index + 1) % PLAYERS

def ask_for_column(player_checker, columns):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if not valid_column_input(user_input, columns):
            print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + columns - 1)}.")
            continue
        col_idx = column_index_from_letter(user_input)
        return col_idx

def main():
    # Validate constants
    if PLAYERS < 2 or PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return
    if COLUMNS < 1 or COLUMNS > 26:
        print("Number of columns must be between 1 and 26.")
        return
    board = create_board(ROWS, COLUMNS)

    # Random first player
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        player_checker = CHECKERS[current_player_idx]
        # Read and validate input with column full check
        col_idx = ask_for_column(player_checker, COLUMNS)

        placed = place_checker(board, col_idx, player_checker)
        if not placed:
            # If column full, player loses turn (skip without re-asking)
            # But we print board and change turn
            print_board(board)
            print(f"Column {chr(ord('A')+col_idx)} is full. Player {player_checker} loses turn.")
            current_player_idx = get_next_player_index(current_player_idx)
            continue
        print_board(board)

        # Check for win after placing
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = get_next_player_index(current_player_idx)

if __name__ == "__main__":
    main()
