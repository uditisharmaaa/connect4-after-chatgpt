import os
import random
import string

# Constants - Change these for different board sizes and number of players
NUM_ROWS = 6
NUM_COLS = 7           # Max 26
NUM_PLAYERS = 2        # 2-5 supported
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    # Print rows (no row labels)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    cols = len(board[0])
    valid = []
    for i in range(cols):
        if board[0][i] == " ":
            valid.append(i)
    return valid

def is_valid_input(inp, board):
    inp = inp.upper()
    if len(inp) != 1:
        return False
    if inp not in string.ascii_uppercase[:len(board[0])]:
        return False
    col_idx = string.ascii_uppercase.index(inp)
    # Check if column is full
    if board[0][col_idx] != " ":
        return False
    return True

def get_column_index(inp):
    return string.ascii_uppercase.index(inp.upper())

def drop_checker(board, col_idx, checker):
    # Place in lowest available space in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Column full, should not happen if validated
    return None, None

def check_win(board, row, col, checker):
    # Check horizontal, vertical, and both diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down right
        (1, -1)   # diag down left
    ]
    for dr, dc in directions:
        count = 1  # counting our latest placed checker
        # Extend in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Extend in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def choose_first_player(num_players):
    return random.randint(0, num_players-1)

def main():
    # Setup
    board = create_board(NUM_ROWS, NUM_COLS)
    player_order = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = choose_first_player(NUM_PLAYERS)
    game_over = False
    winner = None

    while not game_over:
        clear_screen()
        print_board(board)
        current_checker = player_order[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Input loop
        while True:
            user_inp = input("> ").strip().upper()
            if is_valid_input(user_inp, board):
                col_idx = get_column_index(user_inp)
                break
            elif len(user_inp) == 1 and user_inp in string.ascii_uppercase[:NUM_COLS]:
                # Valid column letter but column is full
                print("Column is full! You lose your turn.")
                col_idx = get_column_index(user_inp)
                # Lose turn
                col_full = True
                break
            else:
                print("Invalid input! Please enter a valid column letter (A-G) that is not full.")

        if len(user_inp) == 1 and user_inp in string.ascii_uppercase[:NUM_COLS] and board[0][col_idx] != " ":
            # Lose turn if column is full
            pass
        else:
            row_idx, col_idx = drop_checker(board, col_idx, current_checker)
            # Check for win
            if check_win(board, row_idx, col_idx, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
                winner = current_checker
                continue
            # Check for draw
            if is_board_full(board):
                clear_screen()
                print_board(board)
                print("Game is a draw!")
                game_over = True
                continue

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
