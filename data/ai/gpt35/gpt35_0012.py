import os
import random

# Constants - DO NOT CHANGE FOR SUBMISSION
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players


def clear_screen():
    os.system('clear')


def create_board():
    # Create a ROWS x COLS board filled with " "
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column labels (A, B, C, ...)
    labels = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS))
    print(labels)

    # Print board rows
    line_sep = '+' + '---+' * COLS
    for row in range(ROWS):
        print(line_sep)
        line = '|'
        for col in range(COLS):
            line += ' {} |'.format(board[row][col])
        print(line)
    print(line_sep)


def get_player_input(player, board):
    valid_columns = {chr(ord('A') + i): i for i in range(COLS)}
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single uppercase letter (A-G).")
            continue
        if col_input not in valid_columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A')+COLS-1)}.")
            continue
        col_idx = valid_columns[col_input]
        # Check if column is full
        if board[0][col_idx] != " ":
            # Column full -> turn lost
            print(f"Column {col_input} is full. Turn lost.")
            return None
        return col_idx


def place_checker(board, col_idx, checker):
    # Place the checker at the lowest available row in column col_idx
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    # Should never reach here because check is done before
    return None


def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diag /, diag \
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def check_draw(board):
    # If top row has no empty spaces, board is full -> draw
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    # Random first player index
    current_player_idx = random.randrange(PLAYERS)

    print_board(board)
    # Inform which player starts
    print(f"Player {players[current_player_idx]} starts.")

    while True:
        player = players[current_player_idx]
        col_idx = get_player_input(player, board)

        if col_idx is None:
            # Column full, turn lost, pass to next player
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        row_idx = place_checker(board, col_idx, player)
        print_board(board)

        # Check win
        if check_win(board, row_idx, col_idx, player):
            print(f"Player {player} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
