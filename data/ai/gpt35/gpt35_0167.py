import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
NUM_PLAYERS = 2  # Set to 2 for submission as requested
WIN_COUNT = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = '  ' + '   '.join(chr(ord('A') + c) for c in range(len(board[0])))
    print(header)
    # Print horizontal line
    line = '+---' * len(board[0]) + '+'
    for row in board:
        print(line)
        # Print each cell in row
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(line)

def valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(letter):
    return ord(letter) - ord('A')

def place_checker(board, col, checker):
    # Place checker in lowest empty row of column col
    # Returns True if placed, False if column full
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal down-right (\)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for offset in range(WIN_COUNT):
                if board[r + offset][c + offset] != checker:
                    win = False
                    break
            if win:
                return True

    # Check diagonal up-right (/)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for offset in range(WIN_COUNT):
                if board[r - offset][c + offset] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def check_draw(board):
    # If any ' ' in top row, not draw yet
    # Actually better: if ANY column is not full, not draw yet
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def get_valid_input(prompt, board):
    cols = len(board[0])
    while True:
        user_input = input(prompt).strip()
        if not valid_column(user_input, cols):
            # Invalid format or out of range
            continue
        col_idx = get_column_index(user_input)
        # Check if column is full
        if board[0][col_idx] != ' ':
            # Turn is lost if column full: break here (special case)
            # But per instructions, if column full turn is lost, so we should
            # detect it outside input loop. So here we accept input but handle afterwards.
            return col_idx, True
        return col_idx, False

def main():
    # Setup game
    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        col_idx, col_full = get_valid_input(prompt, board)

        if col_full:
            # Turn lost if column full, do NOT place checker, switch player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col_idx, checker)
        print_board(board)

        if placed:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                print("The game is a draw.")
                break
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            # Should not happen, as we check for col_full above, but safe fallback
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
