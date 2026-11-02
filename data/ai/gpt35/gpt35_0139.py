import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
WIN_COUNT = 4

# Current assignment: 2 players, board 6x7
NUM_PLAYERS = 2
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Use only as many as NUM_PLAYERS

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Print each row with horizontal separators
    horizontal_line = '+' + ('---+' * cols)
    for r in range(rows):
        print(horizontal_line)
        row_cells = [' ' + board[r][c] + ' ' for c in range(cols)]
        print('|' + '|'.join(row_cells) + '|')
    print(horizontal_line)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    c = ord(col_char) - ord('A')
    return 0 <= c < cols

def column_index(col_char):
    return ord(col_char) - ord('A')

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Start from bottom row, place checker in lowest empty cell of column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # Column full, no placement
    return None, None

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # include current checker

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True

    return False

def board_full(board):
    for c in range(len(board[0])):
        if not is_column_full(board, c):
            return False
    return True

def get_valid_input(current_player, cols):
    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, cols):
            print(f"Invalid input. Please enter a letter A-{chr(ord('A')+cols-1)}.")
            continue
        col = column_index(inp)
        if is_column_full(board, col):
            # Turn is lost for this player, per assignment
            return None
        return col

def main():
    global board
    board = create_board(ROWS, COLS)
    players = PLAYERS_CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)  # Show empty board with columns before starting

    while True:
        current_checker = players[current_player_index]
        col = get_valid_input(current_checker, COLS)

        if col is None:
            # Column full, turn lost silently (no repeated prompt)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        row, placed_col = place_checker(board, col, current_checker)
        print_board(board)

        if check_win(board, row, placed_col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
