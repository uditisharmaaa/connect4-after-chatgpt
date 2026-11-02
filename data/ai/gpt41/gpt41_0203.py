import os
import random
import string

# === CONSTANTS ===
ROWS = 6                     # Number of rows
COLUMNS = 7                  # Number of columns, max 26
NUM_PLAYERS = 2              # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

# === UTILITY FUNCTIONS ===

def clear_screen():
    os.system('clear')  # For Unix/Linux/macOS

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    column_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(column_labels))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_next_open_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def is_board_full(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def valid_column_input(user_input, board):
    if len(user_input) != 1 or user_input not in string.ascii_uppercase:
        return False
    col = string.ascii_uppercase.index(user_input)
    if col < 0 or col >= len(board[0]):
        return False
    return True

def place_checker(board, col, checker):
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row, col
    else:
        return None, None

def in_bounds(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def check_direction(board, row, col, d_row, d_col, checker):
    count = 0
    r, c = row, col
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    return count

def check_win(board, row, col, checker):
    # Check all 4 directions: horizontal, vertical, diag1 (\), diag2 (/)
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1
        # check forward
        count += check_direction(board, row+dr, col+dc, dr, dc, checker) - 0
        # check backward
        count += check_direction(board, row-dr, col-dc, -dr, -dc, checker) - 0
        if count >= 4:
            return True
    return False

# === MAIN GAME LOOP ===

def main():
    # Create the board
    board = create_board(ROWS, COLUMNS)
    # Select player checkers
    players = CHECKERS[:NUM_PLAYERS]
    # Pick random first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_screen()
    print_board(board)

    while True:
        checker = players[current_player]
        print(f"Player {checker}, please enter a column:")
        user_input = input("> ").strip().upper()

        # Validate input
        if not valid_column_input(user_input, board):
            print("Invalid input! Please enter a column letter (A to {}).".format(string.ascii_uppercase[COLUMNS-1]))
            continue

        col = string.ascii_uppercase.index(user_input)
        if board[0][col] != " ":
            print("Column is full! You lose your turn.")
            # Lose turn, so skip to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        row, col = place_checker(board, col, checker)
        clear_screen()
        print_board(board)

        # Win check
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Draw check
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
