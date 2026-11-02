import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
CLEAR_COMMAND = 'clear'  # for Linux/Unix terminals

def clear_screen():
    os.system(CLEAR_COMMAND)

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = '  '
    for i in range(len(board[0])):
        header += chr(ord('A') + i) + '   '
    print(header.rstrip())
    # Print rows
    for row in range(len(board)):
        print('+---' * len(board[0]) + '+')
        line = '|'
        for col in range(len(board[0])):
            line += ' ' + board[row][col] + ' |'
        print(line)
    print('+---' * len(board[0]) + '+')

def is_valid_column(col_char, board):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + len(board[0]) - 1)):
        return False
    col_index = ord(col_char) - ord('A')
    # Check if column is full (top row is occupied)
    return board[0][col_index] == ' '

def get_valid_input(player, board):
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, board):
            # Check if column is full or invalid input
            col_index = None
            if len(inp) == 1 and ('A' <= inp <= chr(ord('A') + len(board[0]) - 1)):
                col_index = ord(inp) - ord('A')
                # Column full => lose turn
                if board[0][col_index] != ' ':
                    return inp  # invalid, but lose turn (as per spec)
            print("Invalid input. Please enter a valid column letter with available space.")
            continue
        return inp

def place_checker(board, col_char, checker):
    col = ord(col_char) - ord('A')
    # Place checker in the lowest empty row of that column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    # Column full: cannot place checker (should never be called if validated)
    return False

def check_line_win(line, checker):
    count = 0
    for c in line:
        if c == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for row in range(rows):
        if check_line_win(board[row], checker):
            return True

    # Vertical check
    for col in range(cols):
        col_vals = [board[row][col] for row in range(rows)]
        if check_line_win(col_vals, checker):
            return True

    # Diagonal checks
    # Diagonal "\" direction
    for row in range(rows - WIN_COUNT + 1):
        for col in range(cols - WIN_COUNT + 1):
            line = [board[row + i][col + i] for i in range(WIN_COUNT)]
            if all(c == checker for c in line):
                return True

    # Diagonal "/" direction
    for row in range(WIN_COUNT - 1, rows):
        for col in range(cols - WIN_COUNT + 1):
            line = [board[row - i][col + i] for i in range(WIN_COUNT)]
            if all(c == checker for c in line):
                return True

    return False

def board_full(board):
    # If top row has any empty space, board is not full
    return all(cell != ' ' for cell in board[0])

def main():
    # Setup constants for this assignment
    num_players = 2
    rows = ROWS
    cols = COLS
    players = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player = players[current_player_index]
        col_char = get_valid_input(player, board)
        col_index = ord(col_char) - ord('A')
        # If input is invalid or column full, player loses turn.
        # We interpret invalid input that passes user validation as column full.
        if not is_valid_column(col_char, board):
            # lose turn
            current_player_index = (current_player_index + 1) % num_players
            print_board(board)
            continue

        placed = place_checker(board, col_char, player)
        if not placed:
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % num_players
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_win(board, player):
            print(f"Player {player} won!")
            break

        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
