import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players


def clear_screen():
    os.system('clear')


def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))


def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2-{len(PLAYER_TOKENS)}): "))
            if 2 <= count <= len(PLAYER_TOKENS):
                return count
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_TOKENS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_valid_column(board):
    while True:
        col_input = input(f"Choose a column ({'/'.join(COLUMN_LABELS)}): ").upper()
        if col_input not in COLUMN_LABELS:
            print("Invalid column. Please try again.")
            continue
        col_idx = COLUMN_LABELS.index(col_input)
        if board[0][col_idx] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_idx


def drop_token(board, col, token):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col


def check_direction(board, start_row, start_col, delta_row, delta_col, token):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == token:
        count += 1
        row += delta_row
        col += delta_col
    return count


def check_win(board, row, col, token):
    # Check all directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    for dr, dc in directions:
        # Count tokens in one direction
        count1 = check_direction(board, row, col, dr, dc, token)
        # Count tokens in the opposite direction (excluding starting point)
        count2 = check_direction(board, row - dr, col - dc, -dr, -dc, token)
        if count1 + count2 - 1 >= 4:
            return True
    return False


def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))


def main():
    clear_screen()
    print("Welcome to Connect 4!\n")
    player_count = get_player_count()
    players = PLAYER_TOKENS[:player_count]
    current_player_index = random.randint(0, player_count - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_token = players[current_player_index]
        print(f"Player {current_token}'s turn")

        col = get_valid_column(board)
        row, col = drop_token(board, col, current_token)

        if check_win(board, row, col, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % player_count


if __name__ == "__main__":
    main()
