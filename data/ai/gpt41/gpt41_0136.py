import os
import random
import string

# ------ Global Constants ------
ROWS = 6      # Number of rows
COLS = 7      # Number of columns (Max 26 allowed for column labels A-Z)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

# ------ Functions ------

def clear_screen():
    # Linux/Unix clear screen
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Column headers (A, B, C, ...)
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    print("+" + "---+" * cols)
    for row in board:
        # Print row cells
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_column_input(board):
    cols = len(board[0])
    valid_cols = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        col_input = input(f"Please enter a column ({'/'.join(valid_cols)}): ").strip().upper()
        if len(col_input) == 1 and col_input in valid_cols:
            col_index = valid_cols.index(col_input)
            # Check if the column is full
            if board[0][col_index] != " ":
                print("Column is full. You lose your turn.")
                return None
            else:
                return col_index
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, checker):
    # Place checker in the lowest available spot in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should not be called if column is full
    return None

def check_four_in_a_row(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Direction vectors: (row_inc, col_inc)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    nr += dr
                    nc += dc
    return False

def is_draw(board):
    # If any cell in the top row is empty, board is not full
    return all(cell != " " for cell in board[0])

def main():
    # --- Initialization ---
    board = create_board(ROWS, COLS)
    player_symbols = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {s}" for s in player_symbols]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"{player_names[current_player]} ({player_symbols[current_player]}) is randomly selected to start.")
    input("Press Enter to start the game...")

    game_over = False

    while not game_over:
        print_board(board)
        checker = player_symbols[current_player]
        player_name = player_names[current_player]
        print(f"{player_name} ({checker}),", end=" ")
        col = get_valid_column_input(board)
        if col is None:
            # Turn lost. Go to next player.
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row, col = place_checker(board, col, checker)
        # Check for win
        if check_four_in_a_row(board, checker):
            print_board(board)
            print(f"{player_name} won!")
            game_over = True
            break
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
