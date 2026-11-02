import os
import random
import string

# ========================== #
#        Constants           #
# ========================== #
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Can be changed from 2 to 5 for testing, submission: 2

# ========================== #
#        Functions           #
# ========================== #

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    col_labels = list(string.ascii_uppercase)[:cols]

    print()
    # Print column labels
    print("  ", end='')
    for label in col_labels:
        print(f" {label}  ", end='')
    print()
    # Print horizontal line
    print("+" + "---+" * cols)
    # Print the board rows
    for r in range(rows):
        print("|", end='')
        for c in range(cols):
            print(f" {board[r][c]} |", end='')
        print()
        print("+" + "---+" * cols)

def is_column_valid(user_input, board):
    cols = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    if len(user_input) != 1:
        return False
    if user_input not in col_labels:
        return False
    # Check if column is full
    col_idx = ord(user_input) - ord('A')
    if board[0][col_idx] != ' ':
        return False
    return True

def drop_checker(board, col_label, checker):
    col_idx = ord(col_label) - ord('A')
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx  # Return the placed row and column index
    return None, None  # should not happen if input was validated

def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Diagonal check (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Diagonal check (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r+i][c-i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])  # If top row is full, board is full

def get_next_player_idx(current_idx, num_players):
    return (current_idx + 1) % num_players

def get_valid_input(prompt, board):
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue
        if not is_column_valid(user_input, board):
            cols = len(board[0])
            labels = [chr(ord('A') + i) for i in range(cols)]
            # Distinguish between 'invalid label' and 'column full'
            if user_input not in labels:
                print("Invalid column. Please choose a valid column letter.")
            elif board[0][ord(user_input) - ord('A')] != ' ':
                print("Column is full. Turn is lost.")
                return None  # Turn is lost if column is full
            continue
        return user_input

def main():
    board = create_board(NUM_ROWS, NUM_COLS)

    # Pick players
    players = PLAYERS_CHECKERS[:NUM_PLAYERS]

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    game_over = False

    while not game_over:
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column:")

        user_col = get_valid_input("> ", board)
        if user_col is None:  # Column full, turn is lost
            current_player_idx = get_next_player_idx(current_player_idx, NUM_PLAYERS)
            clear_screen()
            print_board(board)
            continue

        row_idx, col_idx = drop_checker(board, user_col, current_player)
        clear_screen()
        print_board(board)

        # Check for win
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            game_over = True
            break

        # Next player's turn
        current_player_idx = get_next_player_idx(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
