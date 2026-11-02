import os
import random
import string

# ----- CONSTANTS -----
NUM_ROWS = 6
NUM_COLS = 7   # Max is 26 (letters A-Z)
NUM_PLAYERS = 2  # Can be 2 to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

# ----- FUNCTIONS -----

def clear_screen():
    # Clear terminal screen (cross-platform)
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header (A B C ...)
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Top border
    print('+' + '---+' * cols)
    # Rows (do NOT print row labels)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_column_input(current_checker, board):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_letters:
            print(f"Invalid input. Please enter a column letter (A-{valid_letters[-1]}).")
            continue
        col_idx = ord(col_input) - ord('A')
        if board[0][col_idx] != ' ':
            print("Column is full. You lose your turn!")
            return None  # Player loses turn
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker in LOWEST available row in that column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Can't place (shouldn't happen due to validation)

def check_winner(board, row, col, checker):
    # Check all 4 directions: horizontal, vertical, 2 diagonals
    directions = [
        (0, 1),   # horiz right
        (1, 0),   # vert down
        (1, 1),   # diag down-right
        (1, -1)   # diag down-left
    ]

    for dr, dc in directions:
        count = 1  # including placed checker
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    # If top row has any empty cell, board is not full
    return all(cell != ' ' for cell in board[0])

def main():
    # Init board
    board = create_board(NUM_ROWS, NUM_COLS)
    # Select random player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    moves = 0
    winner = None

    while True:
        checker = CHECKERS[current_player]
        col_idx = get_column_input(checker, board)
        if col_idx is not None:
            # Valid move, so place checker
            row_idx, _ = place_checker(board, col_idx, checker)
            moves += 1
            clear_screen()
            print_board(board)
            if check_winner(board, row_idx, col_idx, checker):
                winner = checker
                break
            if board_full(board):
                break
        else:
            # Invalid move: column is full, turn lost
            clear_screen()
            print_board(board)
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
