import os
import random
import string

# CONSTANTS
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    # Print rows with separators
    row_sep = '+' + ('---+' * len(board[0]))
    for row in board:
        print(row_sep)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(row_sep)

def get_valid_column_input(board, player):
    cols = len(board[0])
    valid_cols = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip().upper()
        # Check length and character
        if len(user_input) != 1 or user_input not in valid_cols:
            continue
        col_index = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col_index] != ' ':
            # Full column: player loses turn
            return None
        return col_index

def place_checker(board, col_index, checker):
    # Place checker in the lowest available spot in col_index
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    return None  # Should not happen due to checks

def check_winner(board, last_row, last_col, checker):
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Including last placed checker

        # Check positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True

    return False

def check_draw(board):
    # Draw if no empty spaces in top row
    return all(cell != ' ' for cell in board[0])

def main():
    rows = ROWS
    cols = COLS
    num_players = 2
    if cols > MAX_COLS:
        raise ValueError(f"Maximum columns allowed is {MAX_COLS}")
    if not (MIN_PLAYERS <= num_players <= MAX_PLAYERS):
        raise ValueError(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}")

    players = PLAYERS[:num_players]
    board = create_board(rows, cols)
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Randomly selected Player {players[current_player_index]} to start.")

    while True:
        player = players[current_player_index]

        col_index = get_valid_column_input(board, player)
        if col_index is None:
            # Column full -> player loses turn
            current_player_index = (current_player_index + 1) % num_players
            print_board(board)
            continue

        placed = place_checker(board, col_index, player)
        print_board(board)

        # Check for winner
        if check_winner(board, placed[0], placed[1], player):
            print(f"Player {player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
