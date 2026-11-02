import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players, use first PLAYERS of these
WIN_CONDITION = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    # board[row][col], row 0 is top, row ROWS-1 is bottom
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    line = "+---" * COLUMNS + "+"
    for row in range(ROWS):
        print(line)
        print("| " + " | ".join(board[row]) + " |")
    print(line)

def input_column(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Invalid length
            continue
        if col_input not in COLUMN_LABELS:
            # Not valid column letter
            continue
        col = ord(col_input) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn
            return None
        return col

def place_checker(board, col, checker):
    # Places checker in the lowest empty spot in column col
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # If here, no space (should not happen if checked before)
    return None

def check_win(board, checker, row, col):
    # Check horizontal, vertical, diagonal (2 directions)
    def count_in_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions to check: horizontal, vertical, diag1 (\), diag2 (/)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # Count how many checkers in one direction and the opposite direction
        count = 1  # current checker
        count += count_in_direction(dr, dc)
        count += count_in_direction(-dr, -dc)
        if count >= WIN_CONDITION:
            return True
    return False

def is_board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

# Initialize board
board = create_board()

# Select random starting player index
current_player_index = random.randrange(PLAYERS)
players_checkers = CHECKERS[:PLAYERS]

print_board(board)

# Game loop
while True:
    checker = players_checkers[current_player_index]
    col = input_column(checker)
    if col is None:
        # Column full, lose turn, next player
        current_player_index = (current_player_index + 1) % PLAYERS
        print_board(board)
        continue

    # Place checker
    row, col_placed = place_checker(board, col, checker)
    print_board(board)

    # Check if win
    if check_win(board, checker, row, col_placed):
        print(f"Player {checker} won!")
        break

    # Check draw
    if is_board_full(board):
        print("The game is a draw!")
        break

    # Next player
    current_player_index = (current_player_index + 1) % PLAYERS
