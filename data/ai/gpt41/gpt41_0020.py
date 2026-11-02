import os
import random
import string

# ---- Constants ----
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2

PLAYER_TOKENS = ["X", "O", "V", "H", "M"]  # Up to 5 players
LETTERS = string.ascii_uppercase

# ---- Functions ----

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    header = "  " + "   ".join(LETTERS[:columns])
    print(header)
    # Print top border
    print("+" + "---+" * columns)
    # Print rows
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print("+" + "---+" * columns)

def is_valid_column(input_str, columns):
    if len(input_str) != 1:
        return False
    if input_str not in LETTERS[:columns]:
        return False
    return True

def is_column_full(board, col_idx):
    return all(board[row][col_idx] != " " for row in range(len(board)))

def get_move(board):
    columns = len(board[0])
    while True:
        user_input = input().strip().upper()
        if not is_valid_column(user_input, columns):
            print(f"Invalid input. Please enter one of {LETTERS[:columns]}.")
            continue
        col_idx = LETTERS.index(user_input)
        if is_column_full(board, col_idx):
            print("Column is full. You lose your turn.")
            return None  # Player loses turn if column is full
        return col_idx

def place_checker(board, col_idx, token):
    # Start from the bottom row and find the first empty cell
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = token
            return row, col_idx
    # Should never reach here if is_column_full is checked elsewhere
    return None

def check_win(board, token, win_len=4):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_len + 1):
            if all(board[r][c+i] == token for i in range(win_len)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_len + 1):
            if all(board[r+i][c] == token for i in range(win_len)):
                return True

    # Check diagonal down-right
    for r in range(rows - win_len + 1):
        for c in range(cols - win_len + 1):
            if all(board[r+i][c+i] == token for i in range(win_len)):
                return True

    # Check diagonal up-right
    for r in range(win_len - 1, rows):
        for c in range(cols - win_len + 1):
            if all(board[r-i][c+i] == token for i in range(win_len)):
                return True

    return False

def board_full(board):
    return all(all(cell != " " for cell in row) for row in board)

def get_next_player(curr_idx, num_players):
    return (curr_idx + 1) % num_players

def run_game():
    board = create_board(ROWS, COLUMNS)
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]

    # Randomly choose first player
    curr_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {tokens[curr_player]}, please enter a column:")

    while True:
        col_idx = get_move(board)
        if col_idx is None:
            # Lose turn for choosing full column
            curr_player = get_next_player(curr_player, NUM_PLAYERS)
            print_board(board)
            print(f"Player {tokens[curr_player]}, please enter a column:")
            continue
        # Place checker
        place_checker(board, col_idx, tokens[curr_player])

        print_board(board)
        # Check if player wins
        if check_win(board, tokens[curr_player]):
            print(f"Player {tokens[curr_player]} won!")
            break
        # Check draw
        if board_full(board):
            print("It's a draw!")
            break
        # Next player
        curr_player = get_next_player(curr_player, NUM_PLAYERS)
        print(f"Player {tokens[curr_player]}, please enter a column:")

# ---- Main Guard ----
if __name__ == "__main__":
    run_game()
