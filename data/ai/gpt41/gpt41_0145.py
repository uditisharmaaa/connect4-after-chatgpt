import os
import random

# --- Constants ---
NUM_ROWS = 6         # Number of rows (height)
NUM_COLS = 7         # Number of columns (width)
MAX_COLS = 26        # Maximum allowed columns (for column labels)
NUM_PLAYERS = 2      # Number of players (between 2 and 5)

# The checker symbols for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Functions ---

def clear_screen():
    os.system("clear")  # For Linux/Unix

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers (A, B, ..., G, etc)
    col_letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  ", end="")
    for c in col_letters:
        print(f" {c}  ", end="")
    print()
    print("+" + "---+" * len(board[0]))
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * len(board[0]))

def get_valid_column_input(board):
    col_letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        col_input = input().strip().upper()
        if len(col_input) != 1:
            print("Please enter a single letter corresponding to a column:")
            continue
        if col_input not in col_letters:
            print("Invalid column. Please enter one of these:", " ".join(col_letters))
            continue
        col_idx = ord(col_input) - ord('A')
        # Check if column is full
        if board[0][col_idx] != " ":
            print("That column is full! You lose your turn.")
            return None  # Lose turn if column is full
        return col_idx

def drop_checker(board, col_idx, checker):
    # Place the checker in the lowest empty spot in that column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None, None  # Shouldn't really happen if checked before

def check_win(board, row, col, checker):
    dirs = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down right
        (1, -1),  # Diagonal down left
    ]
    for dr, dc in dirs:
        count = 1
        # Go forward
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Go backward
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def play_game():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]} starts!")

    while True:
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, please enter a column:")
        col_idx = get_valid_column_input(board)
        if col_idx is None:
            # Player loses turn if full column
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row, col = drop_checker(board, col_idx, player_checker)
        clear_screen()
        print_board(board)

        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


# --- Main program ---
if __name__ == "__main__":
    play_game()
