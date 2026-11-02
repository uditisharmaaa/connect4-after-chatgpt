import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2  # For submission: 2 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    # Board: rows of lists with ' ' initial values
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(labels))
    sep_line = '+' + '---+' * cols
    rows = len(board)

    for r in range(rows):
        print(sep_line)
        row_cells = []
        for c in range(cols):
            row_cells.append(' ' + board[r][c] + ' ')
        print('|' + '|'.join(row_cells) + '|')
    print(sep_line)

def is_valid_column(input_str, cols):
    # Valid if input_str length is 1 and A <= input_str <= A+cols-1
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    return 'A' <= c < chr(ord('A') + cols)

def column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available cell in column col_idx
    # Return True if placed, False if column full
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return True
    return False

def board_full(board):
    # If all top row cells occupied -> board full
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Check diagonal down-right
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Check diagonal down-left
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def get_player_input(player_checker, board):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, cols):
            # Invalid letter or length
            continue
        col_idx = column_index(inp)
        if board[0][col_idx] != ' ':
            # Column full; player loses turn (return None)
            return None
        return col_idx

def main():
    # Setup
    board = create_board()
    players = CHECKERS[:PLAYERS_COUNT]

    # Random starting player
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]

        col_choice = get_player_input(current_checker, board)

        if col_choice is None:
            # Column full, player loses turn as per spec
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue

        placed = place_checker(board, col_choice, current_checker)
        if not placed:
            # Should not happen due to earlier check, but safe fallback
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue

        # Check for win
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print_board(board)
            print("Game is a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
