import os
import random
import string

# ---------- CONSTANTS ----------

NUM_ROWS = 6
NUM_COLS = 7  # Max 26
NUM_PLAYERS = 2  # 2-5

PLAYER_MARKS = ["X", "O", "V", "H", "M"] # Only use up to NUM_PLAYERS

# ---------- HELPER FUNCTIONS ----------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Returns a blank 2D list (board)
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column letters
    col_labels = '   '.join(string.ascii_uppercase[:cols])
    print(f"  {col_labels}")
    # Print separator
    print('+' + '---+' * cols)
    # Print rows from top to bottom
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_col_from_input(inp, num_cols):
    """Converts column letter to integer index; returns None if invalid"""
    if len(inp) != 1 or inp not in string.ascii_uppercase[:num_cols]:
        return None
    return ord(inp) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, marker):
    """Place marker in the lowest empty row in the column, return row index or None."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = marker
            return row
    return None

def board_full(board):
    return all(cell != " " for cell in board[0])

def check_win(board, row, col, marker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Count the placed checker itself
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == marker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == marker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def player_name(marker):
    return f"Player {marker}"

# ---------- MAIN GAME ----------

def main():
    # --- Setup ---
    board = create_board(NUM_ROWS, NUM_COLS)
    player_markers = PLAYER_MARKS[:NUM_PLAYERS]
    curr_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"{player_name(player_markers[curr_player_idx])} starts!\n")

    game_over = False
    winner = None

    while not game_over:
        marker = player_markers[curr_player_idx]
        # Get user input loop
        inp_valid = False
        while not inp_valid:
            print(f"{player_name(marker)}, please enter a column:")
            inp = input().strip().upper()
            col = get_col_from_input(inp, NUM_COLS)
            if col is None:
                print("Invalid input: Please enter a valid column letter (e.g. A, B, ...).")
                continue
            if is_column_full(board, col):
                print("Column is full. Your turn is lost!")
                inp_valid = True  # Turn is lost if column is full
                row = None
                col = None
            else:
                row = place_checker(board, col, marker)
                inp_valid = True

        clear_screen()
        print_board(board)

        # Only check for win/draw if a checker was actually placed
        if row is not None:
            # Check for win
            if check_win(board, row, col, marker):
                print(f"{player_name(marker)} won!")
                winner = marker
                game_over = True
                continue
            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                game_over = True
                continue

        # Next player's turn
        curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
