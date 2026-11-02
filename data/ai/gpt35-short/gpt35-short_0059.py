import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players


def clear_screen():
    os.system('clear')


def create_board():
    """Initialize empty board (list of lists)"""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Prints the board with column labels"""
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLUMNS * 2 + 1))


def get_valid_column(prompt, board):
    """Prompt player until a valid column with space is chosen"""
    while True:
        choice = input(prompt).strip().upper()
        if choice not in COLUMN_LABELS:
            print("Invalid column. Choose from A to G.")
            continue

        col_idx = COLUMN_LABELS.index(choice)
        if board[0][col_idx] != ' ':
            print("Column is full. Pick another column.")
            continue

        return col_idx


def drop_piece(board, col_idx, player):
    """Drop player's piece in the lowest available row in chosen column"""
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return row, col_idx


def check_winner(board, row, col, player):
    """Check all directions for 4 in a row"""

    def count_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count current piece
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= 4:
            return True
    return False


def board_full(board):
    """Returns True if no empty spaces in top row"""
    return all(space != ' ' for space in board[0])


def main():
    # Choose number of players
    while True:
        try:
            num_players = int(input(f"Enter number of players (2-{len(PLAYERS)}): "))
            if 2 <= num_players <= len(PLAYERS):
                break
            else:
                print(f"Please enter a number between 2 and {len(PLAYERS)}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    players = PLAYERS[:num_players]

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")

        col_idx = get_valid_column("Choose a column (A-G): ", board)
        row_idx, col_idx = drop_piece(board, col_idx, current_player)

        # Check win
        if check_winner(board, row_idx, col_idx, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
