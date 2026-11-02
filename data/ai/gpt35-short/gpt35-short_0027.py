import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = 'A B C D E F G'.split()
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Use first N of these players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + "   ".join(COLUMNS_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")
    print()

def get_player_count():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def choose_first_player(players):
    first = random.choice(players)
    print(f"\n{first} will start first.\n")
    return first

def is_valid_column(col):
    return col in COLUMNS_LABELS

def get_column_index(col):
    return COLUMNS_LABELS.index(col)

def drop_piece(board, col_index, piece):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = piece
            return row, col_index
    return None  # Column full

def is_board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def check_direction(board, start_row, start_col, delta_row, delta_col, piece):
    count = 0
    row, col = start_row, start_col

    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == piece:
        count += 1
        row += delta_row
        col += delta_col

    return count

def check_win(board, row, col, piece):
    # Check all 4 directions (horizontal, vertical, two diagonals)
    directions = [
        ((0, -1), (0, +1)),   # horizontal
        ((-1, 0), (+1, 0)),   # vertical
        ((-1, -1), (+1, +1)), # diagonal /
        ((-1, +1), (+1, -1)), # diagonal \
    ]

    for dir1, dir2 in directions:
        count = 1  # Include the last placed piece
        count += count_in_direction(board, row, col, dir1[0], dir1[1], piece)
        count += count_in_direction(board, row, col, dir2[0], dir2[1], piece)
        if count >= 4:
            return True
    return False

def count_in_direction(board, start_row, start_col, delta_row, delta_col, piece):
    count = 0
    row = start_row + delta_row
    col = start_col + delta_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == piece:
        count += 1
        row += delta_row
        col += delta_col
    return count

def get_player_input(current_player):
    while True:
        col = input(f"{current_player}'s turn. Choose column (A-G): ").upper()
        if not is_valid_column(col):
            print(f"Invalid column. Choose a letter A-G.")
            continue
        return col

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_player_count()
    players = PLAYERS[:num_players]
    current_player_index = players.index(choose_first_player(players))
    board = create_board()

    while True:
        clear_screen()
        print_board(board)

        col = get_player_input(players[current_player_index])
        col_index = get_column_index(col)
        drop = drop_piece(board, col_index, players[current_player_index])

        if drop is None:
            print(f"Column {col} is full. Try again.")
            input("Press Enter to continue...")
            continue

        row, col_index = drop

        if check_win(board, row, col_index, players[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_index]} wins! Congratulations!")
            break

        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_index = (current_player_index + 1) % num_players

    print("Game over.")

if __name__ == "__main__":
    main()
