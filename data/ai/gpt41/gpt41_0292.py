import os
import random
import string

# ==== Constants ====
NUM_ROWS = 6         # Default board height
NUM_COLS = 7         # Default board width (max 26)
NUM_PLAYERS = 2      # Between 2 and 5
CONNECT_N = 4        # How many in a row needed to win

PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

# ==== Functions ====

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    # Print horizontal line
    print("+" + "---+"*cols)
    for row in board:
        print("|" + "|".join(f" {cell}" for cell in row) + "|")
        print("+" + "---+"*cols)

def get_valid_players(num):
    return PLAYER_TOKENS[:num]

def get_player_name(token):
    return f"Player {token}"

def select_random_player(num_players):
    return random.randint(0, num_players - 1)

def get_player_input(player_token, cols):
    valid_cols = string.ascii_uppercase[:cols]
    while True:
        choice = input(f"{get_player_name(player_token)}, please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in valid_cols:
            print(f"Invalid input. Please enter one of these: {', '.join(valid_cols)}")
            continue
        return valid_cols.index(choice)

def place_checker(board, col, player_token):
    for row in reversed(board):  # Start from bottom
        if row[col] == " ":
            row[col] = player_token
            return True
    return False  # Column is full

def check_win(board, player_token):
    rows = len(board)
    cols = len(board[0])

    # Helper to check a line of CONNECT_N in a direction
    def check_line(start_row, start_col, dr, dc):
        count = 0
        r, c = start_row, start_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_token:
            count += 1
            if count == CONNECT_N:
                return True
            r += dr
            c += dc
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player_token:
                continue
            # Check in all 4 directions
            if (check_line(r, c,  0, 1) or   # Horizontal
                check_line(r, c,  1, 0) or   # Vertical
                check_line(r, c,  1, 1) or   # Diagonal (\)
                check_line(r, c,  1, -1)):   # Diagonal (/)
                return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_tokens = get_valid_players(NUM_PLAYERS)
    current_player_idx = select_random_player(NUM_PLAYERS)

    clear_screen()
    print_board(board)
    print(f"{get_player_name(player_tokens[current_player_idx])} goes first!\n")

    while True:
        player_token = player_tokens[current_player_idx]

        col = get_player_input(player_token, NUM_COLS)
        # Try to place checker; lose turn if column is full
        if not place_checker(board, col, player_token):
            print("Column is full! Turn lost.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, player_token):
            print(f"{get_player_name(player_token)} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
