import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print top border
    print('+' + '---+' * COLS)
    # Print rows from top to bottom
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)


def is_valid_column(col_letter):
    return col_letter in COLUMN_LABELS


def column_index(col_letter):
    return COLUMN_LABELS.index(col_letter)


def place_checker(board, col, checker):
    # Place checker in the lowest available spot in column col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full


def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def board_full(board):
    # If any cell in the top row is empty, board is not full
    for cell in board[0]:
        if cell == ' ':
            return False
    return True


def input_column(current_player):
    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(inp) == 1 and is_valid_column(inp):
            return inp
        # Invalid input message will be implicit by repeating input prompt


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = players[current_player_index]

    print_board(board)

    while True:
        col_letter = input_column(current_checker)
        col = column_index(col_letter)
        row = place_checker(board, col, current_checker)

        if row == -1:
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = players[current_player_index]
            print_board(board)
            continue

        print_board(board)

        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = players[current_player_index]


if __name__ == "__main__":
    main()
