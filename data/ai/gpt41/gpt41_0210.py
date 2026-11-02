import os
import random
import string

# ----------------------
# CONSTANTS (Can be adjusted for other dimensions/players)
NUM_ROWS = 6
NUM_COLS = 7        # Max 26 supported (A-Z)
NUM_PLAYERS = 2     # Can be 2-5

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# ----------------------
# Initialize the board as empty
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# ----------------------
# Print the board in the specified format
def print_board(board):
    os.system('clear')  # For Linux/Mac, on Windows use os.system('cls')
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

# ----------------------
# Get valid player input and validate it
def get_player_move(board, player_symbol):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        move = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in valid_letters:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col_idx = ord(move) - ord('A')
        # Check if column is full
        if board[0][col_idx] != " ":
            print("Column is full! You lose your turn.")
            return None
        return col_idx

# ----------------------
# Place a checker for player in the column, returns the row where placed (or None if error)
def place_checker(board, col_idx, player_symbol):
    rows = len(board)
    for row in range(rows-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = player_symbol
            return row
    # Should not reach here if checked before
    return None

# ----------------------
# Check if a certain player has 4 in a row from the last placed position
def check_win(board, row_idx, col_idx, player_symbol):
    return (check_direction(board, row_idx, col_idx, player_symbol, 0, 1)   # horizontal
         or check_direction(board, row_idx, col_idx, player_symbol, 1, 0)   # vertical
         or check_direction(board, row_idx, col_idx, player_symbol, 1, 1)   # diagonal /
         or check_direction(board, row_idx, col_idx, player_symbol, 1, -1)) # diagonal \

# Count consecutive symbols in a direction
def check_direction(board, row, col, symbol, d_row, d_col):
    rows = len(board)
    cols = len(board[0])
    count = 1

    # Check in positive direction (d_row, d_col)
    r, c = row + d_row, col + d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += d_row
        c += d_col

    # Check in negative direction (-d_row, -d_col)
    r, c = row - d_row, col - d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r -= d_row
        c -= d_col

    return count >= 4

# ----------------------
# Check if the board is full (draw)
def check_draw(board):
    return all(cell != " " for cell in board[0])

# ----------------------
def main():
    # Use only as many player symbols as the number of players
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # RANDOMLY CHOOSE STARTING PLAYER
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial (empty) board
    print_board(board)

    while True:
        player_symbol = player_symbols[current_player_idx]
        move = get_player_move(board, player_symbol)

        # If move is None, player's turn is lost (column full)
        if move is not None:
            row_placed = place_checker(board, move, player_symbol)
            print_board(board)

            # Check for win
            if check_win(board, row_placed, move, player_symbol):
                print(f"Player {player_symbol} won!")
                break

            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                break
        else:
            print_board(board) # Still print board if turn is lost

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# ----------------------
if __name__ == "__main__":
    main()
