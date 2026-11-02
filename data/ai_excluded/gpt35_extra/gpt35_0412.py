import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # maximum columns supported by letters A-Z
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
NUM_PLAYERS = 2  # must be 2 for submission as per instructions


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    board = [[' ' for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    columns = len(board[0])
    rows = len(board)
    header = '  ' + '   '.join(string.ascii_uppercase[:columns])
    line = '+' + '---+' * columns
    print(header)
    print(line)
    for row in range(rows):
        row_str = '|'
        for col in range(columns):
            row_str += ' ' + board[row][col] + ' |'
        print(row_str)
        print(line)


def get_valid_input(current_player, board):
    columns = len(board[0])
    valid_letters = string.ascii_uppercase[:columns]

    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter exactly one letter corresponding to a column.")
            continue
        if inp not in valid_letters:
            print(f"Invalid column. Please enter a column between A and {valid_letters[-1]}.")
            continue
        col = valid_letters.index(inp)
        if board[0][col] != ' ':
            # Column is full, player loses turn
            return None
        return col


def place_checker(board, col, checker):
    rows = len(board)
    # place checker in lowest available row in column col
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # if column full, return None
    return None


def check_winner(board, checker, row, col):
    """
    Check if placing checker at board[row][col] creates a 4-in-a-row horizontally, vertically or diagonally
    """
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
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

        if count >= WIN_COUNT:
            return True
    return False


def board_full(board):
    # If top row has any empty cell, board not full
    return all(cell != ' ' for cell in board[0])


def main():
    # Initialize
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS[:NUM_PLAYERS]

    current_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        current_player = players[current_idx]
        col = get_valid_input(current_player, board)
        if col is None:
            # column full, lose turn
            clear_screen()
            print_board(board)
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        pos = place_checker(board, col, current_player)
        clear_screen()
        print_board(board)

        if check_winner(board, current_player, pos[0], pos[1]):
            print(f"Player {current_player} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == '__main__':
    main()
