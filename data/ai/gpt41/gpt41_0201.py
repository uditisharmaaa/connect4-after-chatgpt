import os
import random

# === Constants ===
ROWS = 6                # number of rows
COLUMNS = 7             # number of columns
MAX_COLUMNS = 26        # for labeling columns A-Z
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # In order, supports up to 5 players
NUM_PLAYERS = 2         # Change this value (2-5) for more players

# === Functions ===

def clear_screen():
    os.system('clear')  # For Linux/Unix terminal

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column letters
    header = "  "
    for col in range(len(board[0])):
        header += chr(ord('A') + col) + "   "
    print(header)
    # Print top separator
    print("+" + "---+" * len(board[0]))
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" {} |".format(cell), end="")
        print()
        print("+" + "---+" * len(board[0]))

def get_valid_column_input(board):
    columns = len(board[0])
    valid_inputs = [chr(ord('A') + i) for i in range(columns)]
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_inputs:
            print("Invalid input! Please enter a valid column letter (A-{}).".format(valid_inputs[-1]))
            continue
        col_index = ord(user_input) - ord('A')
        if board[0][col_index] != " ":
            print("That column is full! Pick another column. (Turn lost)")
            return None  # Column is full, turn is lost
        return col_index

def drop_checker(board, col, player_char):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player_char
            return True
    return False  # Should NOT happen if input is validated

def check_for_win(board, player_char):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player_char:
                continue
            # Check right
            if c + 3 < cols and all(board[r][c+i] == player_char for i in range(4)):
                return True
            # Check down
            if r + 3 < rows and all(board[r+i][c] == player_char for i in range(4)):
                return True
            # Check diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == player_char for i in range(4)):
                return True
            # Check diagonal down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == player_char for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    # Setup
    rows = ROWS
    columns = COLUMNS
    num_players = NUM_PLAYERS
    if num_players > len(PLAYER_TOKENS):
        num_players = len(PLAYER_TOKENS)
    player_chars = PLAYER_TOKENS[:num_players]
    board = create_board(rows, columns)
    # Choose first player at random
    current_player = random.randint(0, num_players-1)
    clear_screen()
    print_board(board)
    winner = None

    while True:
        print("Player {}, your turn.".format(player_chars[current_player]))
        col = get_valid_column_input(board)
        if col is not None:
            drop_checker(board, col, player_chars[current_player])
            clear_screen()
            print_board(board)
            if check_for_win(board, player_chars[current_player]):
                print("Player {} won!".format(player_chars[current_player]))
                winner = player_chars[current_player]
                break
            elif check_for_draw(board):
                print("Game is a draw!")
                break
        # If col is None, turn is lost (as per assignment)
        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
