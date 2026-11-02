import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # To support beyond 7 columns if needed
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # 'A' to 'G'

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(COLUMN_LABELS))  # Print column headers
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if the column is valid and has empty space
def is_valid_column(board, col_index):
    return 0 <= col_index < COLUMNS and board[0][col_index] == " "

# Drop the checker into the column at the lowest available row
def drop_checker(board, col_index, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row  # Return the row where the checker was placed

# Check for a win in all directions
def check_for_win(board, row, col, symbol):
    def count_consecutive(delta_row, delta_col):
        count = 0
        r, c = row, col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check horizontal, vertical, and diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if count_consecutive(dr, dc) + count_consecutive(-dr, -dc) - 1 >= 4:
            return True
    return False

# Check if the board is full
def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    player_symbols = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {player_symbols[current_player]} goes first!\n")

    while True:
        # Prompt current player for input
        print_board(board)
        column = input(f"Player {player_symbols[current_player]}, please enter a column: ").strip().upper()

        # Validate input
        if len(column) != 1 or column not in COLUMN_LABELS:
            print("Invalid input. Please enter a valid column (e.g., A-G).")
            continue

        col_index = COLUMN_LABELS.index(column)
        if not is_valid_column(board, col_index):
            print("Invalid move. Column is full or out of bounds.")
            continue

        # Place the checker
        row_index = drop_checker(board, col_index, player_symbols[current_player])

        # Check for a win or draw
        if check_for_win(board, row_index, col_index, player_symbols[current_player]):
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
