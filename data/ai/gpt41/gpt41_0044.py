import os
import random
import sys

# ----- Constants -----
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
MAX_COLS = 26
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

# ----- Functions -----

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column names
    print("  " + "   ".join(COLUMN_LABELS[:COLS]))
    print("+" + "---+" * COLS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column(board, input_prompt):
    while True:
        col_input = input(input_prompt)
        if len(col_input) != 1 or not col_input.isalpha() or not col_input.isupper():
            print("Invalid input. Please enter a single uppercase letter for the column.")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Choose between A and {chr(ord('A') + COLS - 1)}.")
            continue
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn!")
            return None  # Indicate lost turn
        return col_index

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not occur due to previous validity checks

def check_win(board, row, col, checker):
    return (check_line(board, row, col, checker, 0, 1) or  # horizontal
            check_line(board, row, col, checker, 1, 0) or  # vertical
            check_line(board, row, col, checker, 1, 1) or  # diag down-right
            check_line(board, row, col, checker, 1, -1))   # diag down-left

def check_line(board, row, col, checker, delta_row, delta_col):
    count = 1
    # Check one direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    # Check opposite direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col
    return count >= 4

def board_full(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_next_player(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    # Random first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Randomly selected: Player {players[current_player]} starts!")
    
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")
        col = get_valid_column(board, "> ")
        if col is None:
            # Full column, player loses turn
            current_player = get_next_player(current_player, NUM_PLAYERS)
            continue
        row, _ = place_checker(board, col, players[current_player])
        if check_win(board, row, col, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        # Next player's turn
        current_player = get_next_player(current_player, NUM_PLAYERS)

if __name__ == '__main__':
    main()
