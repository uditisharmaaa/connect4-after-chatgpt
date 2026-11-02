import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    """Creates a ROWS x COLUMNS board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect4 board with column labels."""
    print(" " + "   ".join(COLUMN_LABELS))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-" * (COLUMNS * 4 + 1))

def get_num_players():
    """Ask the user for the number of players (2-5)."""
    while True:
        try:
            num = int(input("Enter number of players (2-5): "))
            if 2 <= num <= 5:
                return num
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def get_player_move(current_player_symbol, board):
    """Ask current player for a valid column to drop their chip."""
    valid_columns = [c for c in COLUMN_LABELS if board[0][COLUMN_LABELS.index(c)] == ' ']
    while True:
        move = input(f"Player {current_player_symbol}, choose a column ({', '.join(valid_columns)}): ").upper()
        if move in valid_columns:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid move. Please select a non-full column from the available options.")

def make_move(board, col, symbol):
    """Drop the player's symbol into the chosen column. Returns the row index it landed on."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    # Should never get here if move is validated before

def check_win(board, row, col, symbol):
    """Check for 4 in a row horizontally, vertically, or diagonally."""
    def count_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check all directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    for dr, dc in directions:
        # Count in positive direction + negative direction + 1 (current)
        total = 1 + count_direction(dr, dc) + count_direction(-dr, -dc)
        if total >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full and no more moves are possible."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_symbol = players[current_player_index]

        col = get_player_move(current_symbol, board)
        row = make_move(board, col, current_symbol)

        if check_win(board, row, col, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
