import os
import random
import sys

# Constants - for submission must be:
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create and return an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board, with column labels A..Z and row separators."""
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print the board with separators
    for row in board:
        print("+" + "---+" * cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * cols)

def input_column(player_checker, cols, board):
    """Prompt player for a valid column input; returns column index or None if full."""
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        print(f"Player {player_checker}, please enter a column:")
        user_input = input().strip().upper()
        if len(user_input) != 1 or user_input not in valid_letters:
            continue  # invalid input, ask again
        col = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full means player loses turn
            return None
        return col

def place_checker(board, col, checker):
    """Place the checker in the lowest empty spot in the column."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # column full

def check_win(board, last_row, last_col, checker):
    """Check if placing checker at (last_row, last_col) makes the player win."""
    rows = len(board)
    cols = len(board[0])
    
    def count_direction(dr, dc):
        count = 0
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # directions to check: horizontal, vertical, two diagonals
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        # count to one side + the other side + 1 for the current position
        total = 1 + count_direction(dr, dc) + count_direction(-dr, -dc)
        if total >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    """Check if board is full (no empty spaces on top row)."""
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        player_checker = players[current_player_index]

        col = input_column(player_checker, COLS, board)
        if col is None:
            # column full, player loses turn (no checker placed)
            # switch player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        row, _ = place_checker(board, col, player_checker)
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            sys.exit()

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            sys.exit()

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
