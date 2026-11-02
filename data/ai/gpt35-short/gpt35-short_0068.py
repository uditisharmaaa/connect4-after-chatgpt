import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

# Set number of players (2 to 5)
NUM_PLAYERS = 4  # Change this value as needed between 2 and 5
PLAYERS = PLAYER_MARKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board():
    # Create a ROWS x COLS board filled with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COL_LABELS))
    # Print board rows from top to bottom
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--'*COLS + '-')  # Bottom border


def get_valid_column_input(player):
    while True:
        user_input = input(f"Player {player}'s turn. Choose a column (A-G): ").strip().upper()
        if user_input not in COL_LABELS:
            print(f"Invalid input. Please enter a letter from A to G.")
            continue
        col = COL_LABELS.index(user_input)
        return col


def drop_piece(board, col, player):
    # Drop piece in the lowest empty row in given column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col
    return None  # Col full


def is_winning_move(board, row, col, player):
    # Check all directions for a connect 4
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def is_board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))


def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS -1)
    clear_screen()
    print(f"Welcome to Connect 4! Players: {', '.join(PLAYERS)}")
    print(f"Player {PLAYERS[current_player_index]} goes first.\n")

    while True:
        print_board(board)
        col = get_valid_column_input(PLAYERS[current_player_index])

        # Check if column is full
        if board[0][col] != ' ':
            clear_screen()
            print(f"Column {COL_LABELS[col]} is full! Try another column.")
            continue

        row, col = drop_piece(board, col, PLAYERS[current_player_index])
        clear_screen()

        if is_winning_move(board, row, col, PLAYERS[current_player_index]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_index]} wins! Congratulations!")
            break

        if is_board_full(board):
            print_board(board)
            print("Game is a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
