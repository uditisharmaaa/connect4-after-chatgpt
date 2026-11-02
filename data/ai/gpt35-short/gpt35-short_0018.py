import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Players to choose from
POSSIBLE_PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """
    Clears the terminal screen to keep the UI clean.
    """
    os.system('clear')  # for Mac/Linux; use 'cls' for Windows if needed

def create_board():
    """
    Creates a new empty board represented by a 2D list filled with spaces.
    """
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """
    Prints the current board with column labels.
    The bottom row is row 0 (visually the bottom of the board).
    """
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    # Print rows from top to bottom
    for row in reversed(range(ROWS)):
        row_str = "| " + " | ".join(board[row]) + " |"
        print(row_str)
        print("+" + "---+" * COLUMNS)

def is_valid_column(col_char):
    """
    Check if the entered column character is valid (A-G).
    """
    return col_char.upper() in COLUMN_LABELS

def get_column_index(col_char):
    """
    Converts the column label (A-G) to a board column index (0-6).
    """
    return COLUMN_LABELS.index(col_char.upper())

def is_column_full(board, col):
    """
    Checks if a column is full (i.e., no empty spaces at the top).
    """
    return board[ROWS - 1][col] != ' '

def drop_piece(board, col, piece):
    """
    Drops a piece into the given column.
    Returns the row where the piece landed, or -1 if column is full.
    """
    for row in range(ROWS):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row
    return -1  # full column

def check_direction(board, start_row, start_col, delta_row, delta_col, piece):
    """
    Count consecutive pieces from start position in a specific direction.
    """
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == piece:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, piece):
    """
    Checks all directions for a winning condition (4 in a row).
    """
    # Check horizontal (left + right), vertical (down only), diagonal /
    # and diagonal \ directions.

    # Horizontal: count pieces left and right
    count = (check_direction(board, row, col, 0, -1, piece) +
             check_direction(board, row, col, 0, 1, piece) - 1)
    if count >= 4:
        return True

    # Vertical: count pieces downward only (since pieces stack)
    count = check_direction(board, row, col, -1, 0, piece)
    if count >= 4:
        return True

    # Diagonal \ (down-left and up-right)
    count = (check_direction(board, row, col, -1, -1, piece) +
             check_direction(board, row, col, 1, 1, piece) - 1)
    if count >= 4:
        return True

    # Diagonal / (up-left and down-right)
    count = (check_direction(board, row, col, 1, -1, piece) +
             check_direction(board, row, col, -1, 1, piece) - 1)
    if count >= 4:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is full (draw).
    """
    for col in range(COLUMNS):
        if not is_column_full(board, col):
            return False
    return True

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    # Ask user for number of players (2 to 5)
    while True:
        try:
            num_players = int(input(f"Enter number of players (2-{len(POSSIBLE_PLAYERS)}): "))
            if 2 <= num_players <= len(POSSIBLE_PLAYERS):
                break
            else:
                print("Invalid number of players. Try again.")
        except ValueError:
            print("Please enter a valid integer.")

    players = POSSIBLE_PLAYERS[:num_players]

    # Select random first player
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        current_piece = players[current_player_index]
        print(f"Player {current_piece}'s turn.")

        # Input for column
        while True:
            col_input = input(f"Choose a column ({', '.join(COLUMN_LABELS)}): ").strip().upper()
            if not is_valid_column(col_input):
                print(f"Invalid input: Choose a letter A to G.")
                continue
            col = get_column_index(col_input)
            if is_column_full(board, col):
                print("That column is full. Pick another one.")
            else:
                break

        row_placed = drop_piece(board, col, current_piece)

        # Check for win condition
        if check_win(board, row_placed, col, current_piece):
            clear_screen()
            print_board(board)
            print(f"Player {current_piece} wins! Congratulations!")
            game_over = True
            continue

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more moves left.")
            game_over = True
            continue

        # Move to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
