import os
import random
import string

# Constants
NUM_ROWS = 6                # Default rows for submission
NUM_COLS = 7                # Default cols for submission
MAX_COLS = 26
PLAYERS = 2                 # Submit with 2 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    # Clear terminal (cross-platform)
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Column labels
    labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep_line = '+' + '---+' * cols
    print(labels)
    print(sep_line)
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print(sep_line)

def get_valid_column_input(num_cols):
    while True:
        col_letter = input('Please enter a column: ').upper()
        if (len(col_letter) == 1 and
            col_letter in string.ascii_uppercase[:num_cols]):
            return string.ascii_uppercase.index(col_letter)
        else:
            print(f"Invalid input. Please enter a letter between A and {string.ascii_uppercase[num_cols-1]}.")

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Place checker in lowest empty location
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not reach here if checked with is_column_full

def check_win(board, row, col, checker, to_win=4):
    directions = [
        (0, 1),   # Horizontal →
        (1, 0),   # Vertical ↓
        (1, 1),   # Diagonal ↘
        (1, -1)   # Diagonal ↙
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= to_win:
            return True
    return False

def is_board_full(board):
    # If top row is full, the board is full.
    return all(cell != ' ' for cell in board[0])

def main():
    # Set up players/checkers
    num_players = PLAYERS
    if num_players > len(CHECKERS) or num_players < 2 or NUM_COLS > MAX_COLS:
        print("Invalid game configuration.")
        return
    player_checkers = CHECKERS[:num_players]

    # Create board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Select random starting player
    current_player = random.randint(0, num_players - 1)

    # Game loop
    winner = None
    while True:
        clear_screen()
        print_board(board)
        checker = player_checkers[current_player]
        print(f"Player {checker},", end=' ')
        col = get_valid_column_input(NUM_COLS)

        if is_column_full(board, col):
            print("Column is full! You lose your turn.")
        else:
            row, _ = place_checker(board, col, checker)
            if check_win(board, row, col, checker, 4):
                clear_screen()
                print_board(board)
                print(f"Player {checker} won!")
                break
            if is_board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break
        # Next player
        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
