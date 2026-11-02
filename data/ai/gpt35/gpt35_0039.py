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
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print the board rows
    for row in range(ROWS):
        print("+---"*COLUMNS + "+")
        line = "|"
        for col in range(COLUMNS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+---"*COLUMNS + "+")

def input_valid(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter exactly one letter corresponding to a column.")
            continue
        if inp not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col = COLUMN_LABELS.index(inp)
        if board[0][col] != " ":  # column full
            print("Column is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in lowest empty spot in column col
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not happen if input_valid checked column properly

def check_win(board, row, col, checker):
    # Check horizontally
    count = 0
    for c in range(COLUMNS):
        count = count + 1 if board[row][c] == checker else 0
        if count >= WIN_COUNT:
            return True

    # Check vertically
    count = 0
    for r in range(ROWS):
        count = count + 1 if board[r][col] == checker else 0
        if count >= WIN_COUNT:
            return True

    # Check diagonal top-left to bottom-right
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    count = 0
    while start_r < ROWS and start_c < COLUMNS:
        count = count + 1 if board[start_r][start_c] == checker else 0
        if count >= WIN_COUNT:
            return True
        if board[start_r][start_c] != checker:
            count = 0
        start_r += 1
        start_c += 1

    # Check diagonal bottom-left to top-right
    start_r = row
    start_c = col
    while start_r < ROWS - 1 and start_c > 0:
        start_r += 1
        start_c -= 1
    count = 0
    while start_r >= 0 and start_c < COLUMNS:
        count = count + 1 if board[start_r][start_c] == checker else 0
        if count >= WIN_COUNT:
            return True
        if board[start_r][start_c] != checker:
            count = 0
        start_r -= 1
        start_c += 1

    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True


# --- MAIN PROGRAM ---

board = create_board()
players = CHECKERS[:PLAYERS_COUNT]

# Randomly select first player
current_player_index = random.randint(0, PLAYERS_COUNT - 1)

print_board(board)

while True:
    player_checker = players[current_player_index]

    col = None
    # Attempt player turn input once; if column full, turn lost, no re-try
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter exactly one letter corresponding to a column.")
            continue
        if inp not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col = COLUMN_LABELS.index(inp)
        if board[0][col] != " ":
            print("Column is full. You lose your turn.")
            col = None
        break

    if col is not None:
        r, c = place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, r, c, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break
    else:
        print_board(board)

    # Next player's turn
    current_player_index = (current_player_index + 1) % PLAYERS_COUNT
