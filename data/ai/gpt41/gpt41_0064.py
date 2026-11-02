import os
import random
import string

# ====== CONSTANTS ======
NUM_ROWS = 6
NUM_COLS = 7  # Max allowed is 26 (A-Z)
NUM_PLAYERS = 2  # Range: 2-5
CHECKERS = ["X", "O", "V", "H", "M"]

# ====== FUNCTIONS ======

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        row_str = "|" + "|".join(" {} ".format(cell) for cell in row) + "|"
        print(row_str)
        print("+" + "---+" * cols)

def get_valid_column(board, prompt):
    cols = len(board[0])
    allowed_columns = string.ascii_uppercase[:cols]
    while True:
        col_in = input(prompt).strip().upper()
        if len(col_in) != 1:
            print("Invalid input: Please enter a single column letter (A-{}).".format(allowed_columns[-1]))
            continue
        if col_in not in allowed_columns:
            print("Invalid column: Please enter a column between A and {}.".format(allowed_columns[-1]))
            continue
        col_idx = allowed_columns.index(col_in)
        # Check if column is not full
        if board[0][col_idx] != " ":
            print("Column {} is full! You lose your turn.".format(col_in))
            return None  # Return None to indicate full column (loses turn)
        return col_idx

def place_checker(board, col, checker):
    rows = len(board)
    # Place from bottom up
    for row in range(rows-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should not get here if called with valid col
    return None

def check_line(line, checker):
    count = 0
    for cell in line:
        count = count + 1 if cell == checker else 0
        if count == 4:
            return True
    return False

def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    # Check rows
    for r in range(rows):
        if check_line(board[r], checker):
            return True
    # Check columns
    for c in range(cols):
        col_line = [board[r][c] for r in range(rows)]
        if check_line(col_line, checker):
            return True
    # Check diagonals (two directions)
    # Bottom left to top right (/)
    for r in range(rows):
        for c in range(cols):
            if (r <= rows - 4) and (c <= cols - 4):
                if all(board[r + i][c + i] == checker for i in range(4)):
                    return True
            # Top left to bottom right (\)
            if (r >= 3) and (c <= cols - 4):
                if all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    # If the top row has any empty, not a draw
    return all(cell != " " for cell in board[0])

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def main():
    # Prepare
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = NUM_PLAYERS
    player_checkers = CHECKERS[:num_players]
    player_names = ["Player {}".format(c) for c in player_checkers]
    current_player = choose_first_player(num_players)

    # Initial print
    clear_screen()
    print_board(board)

    while True:
        checker = player_checkers[current_player]
        player_str = player_names[current_player]
        print("{} ({}), please enter a column:".format(player_str, checker))
        col_idx = get_valid_column(board, "")
        if col_idx is None:
            # column full, lose turn
            current_player = (current_player + 1) % num_players
            clear_screen()
            print_board(board)
            continue
        # Place checker
        place_checker(board, col_idx, checker)
        clear_screen()
        print_board(board)
        # Check win
        if check_win(board, checker):
            print("{} won!".format(player_str))
            break
        # Check draw
        if is_draw(board):
            print("It's a draw!")
            break
        # Next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
