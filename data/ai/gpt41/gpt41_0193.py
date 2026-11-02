import os
import random
import string

# Constants (change if needed)
ROWS = 6
COLUMNS = 7
MAX_COLS = 26
NUM_PLAYERS = 2  # between 2 and 5

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows if needed

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    # Print column letters
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(labels))
    print("+" + "---+" * cols)
    for row in board:
        print("|" + "|".join(" " + cell + " " for cell in row) + "|")
        print("+" + "---+" * cols)

def get_valid_input(prompt, valid_columns):
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1:
            print("Invalid input! Enter a single column letter.")
            continue
        if user_input not in valid_columns:
            print("Invalid column! Please choose a valid column letter.")
            continue
        return user_input

def is_column_full(board, col_idx):
    return all(board[row][col_idx] != " " for row in range(ROWS))

def place_checker(board, col_idx, checker):
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # This should not happen if checked before

def check_victory(board, last_row, last_col, checker):
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down right
        (1, -1)  # diagonal down left
    ]
    for dr, dc in directions:
        count = 1  # Count this piece
        # Check in positive direction
        r, c = last_row+dr, last_col+dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row-dr, last_col-dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    if COLUMNS > MAX_COLS:
        print(f"Max columns supported: {MAX_COLS}")
        return

    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)
    col_labels = [string.ascii_uppercase[i] for i in range(COLUMNS)]
    player_idx = random.randint(0, NUM_PLAYERS-1)

    clear_screen()
    print_board(board, COLUMNS)

    while True:
        checker = checkers[player_idx]
        print(f"Player {checker}, please enter a column:")
        col_letter = get_valid_input("> ", col_labels)
        col_idx = col_labels.index(col_letter)
        if is_column_full(board, col_idx):
            print("Column full! You lose your turn.")
            player_idx = (player_idx + 1) % NUM_PLAYERS
            input("Press enter to continue...")
            clear_screen()
            print_board(board, COLUMNS)
            continue
        row_idx, _ = place_checker(board, col_idx, checker)
        clear_screen()
        print_board(board, COLUMNS)
        if check_victory(board, row_idx, col_idx, checker):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        player_idx = (player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
