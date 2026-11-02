import os
import random
import sys

# ---------- Constants ----------
ROWS = 6
COLUMNS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']   # Up to 5 players
NUM_PLAYERS = 2                            # For submission, change as needed (2-5)
WIN_COUNT = 4                              # Number of checkers in a row needed to win
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]  # ['A', 'B', 'C', ...]
EMPTY_CELL = ' '

# ---------- Functions ----------

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    # Create and return board initialized to empty spaces
    return [[EMPTY_CELL for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_next_open_row(board, col):
    # Return the lowest available row (biggest index) in column col, or None if full
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def is_valid_column(input_str):
    # Check if input corresponds to a valid column letter
    return input_str in COLUMN_LABELS

def board_full(board):
    # If no cell is empty in the top row, board is full
    for col in range(COLUMNS):
        if board[0][col] == EMPTY_CELL:
            return False
    return True

def place_checker(board, row, col, token):
    board[row][col] = token

def check_win(board, row, col, token):
    # Check all directions for WIN_COUNT in a row for token starting at (row, col)
    return (check_direction(board, row, col, token, 0, 1) or  # Horizontal
            check_direction(board, row, col, token, 1, 0) or  # Vertical
            check_direction(board, row, col, token, 1, 1) or  # Diagonal /
            check_direction(board, row, col, token, 1, -1))   # Diagonal \

def check_direction(board, row, col, token, d_row, d_col):
    count = 1
    # Check forward direction
    r, c = row + d_row, col + d_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == token:
        count += 1
        r += d_row
        c += d_col
    # Check backward direction
    r, c = row - d_row, col - d_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == token:
        count += 1
        r -= d_row
        c -= d_col
    return count >= WIN_COUNT

def get_player_input(player_token, board):
    while True:
        col_input = input(f"Player {player_token}, please enter a column: ").strip().upper()
        if not is_valid_column(col_input):
            print("Invalid column. Please choose a letter between {} and {}.".format(COLUMN_LABELS[0], COLUMN_LABELS[-1]))
            continue
        col = COLUMN_LABELS.index(col_input)
        if board[0][col] != EMPTY_CELL:
            print("That column is full. You lose your turn.")
            return None   # Losing the turn
        return col

def pick_starting_player():
    return random.randint(0, NUM_PLAYERS - 1)

def available_players():
    return PLAYER_TOKENS[:NUM_PLAYERS]

def main():
    board = create_board()
    players = available_players()
    turn = pick_starting_player()
    clear_screen()
    print_board(board)

    while True:
        player = players[turn]
        col = get_player_input(player, board)
        if col is None:
            # Column full: lose turn
            turn = (turn + 1) % NUM_PLAYERS
            continue

        row = get_next_open_row(board, col)
        if row is not None:
            place_checker(board, row, col, player)
            clear_screen()
            print_board(board)
            # Check for win
            if check_win(board, row, col, player):
                print(f"Player {player} won!")
                break
            # Check for draw
            if board_full(board):
                print("It's a draw!")
                break
            # Alternate to next player
            turn = (turn + 1) % NUM_PLAYERS
        else:
            # Should not happen due to validation in get_player_input
            print("Column is full. You lose your turn.")
            turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
