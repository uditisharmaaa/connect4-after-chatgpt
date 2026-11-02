import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Player pieces - first N pieces will be used according to NUM_PLAYERS
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Set number of players here (2 to 5)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create a 6x7 board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and current pieces."""
    clear_screen()
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))  # Bottom border

def is_valid_column(col_index, board):
    """Check if a move in column col_index is valid (column not full)."""
    return board[0][col_index] == ' '

def get_next_open_row(col_index, board):
    """Return the lowest empty row index in the given column."""
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    """Place the player's piece on the board at the specified row and column."""
    board[row][col] = piece

def winning_move(board, piece):
    """Check if placing 'piece' causes a win horizontally, vertically or diagonally."""

    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and board[r][c+1] == piece and
                board[r][c+2] == piece and board[r][c+3] == piece):
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and board[r+1][c] == piece and
                board[r+2][c] == piece and board[r+3][c] == piece):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == piece and board[r+1][c+1] == piece and
                board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and board[r-1][c+1] == piece and
                board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True

    return False

def is_draw(board):
    """Check if the board is completely full - draw."""
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_player_move(player_piece):
    """
    Prompt player for input and validate:
    - Input must be one of A-G (case insensitive)
    - The column must not be full
    """
    while True:
        choice = input(f"Player {player_piece}, choose a column (A-G): ").strip().upper()
        if choice in COLUMN_LABELS:
            col_index = COLUMN_LABELS.index(choice)
            return col_index
        else:
            print(f"Invalid input. Please enter one of {', '.join(COLUMN_LABELS)}.")

def main():
    # Initialize board and players
    board = create_board()
    players = PLAYER_PIECES[:NUM_PLAYERS]

    # Randomly pick starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        player_piece = players[current_player_index]

        # Get valid move column from player
        while True:
            col = get_player_move(player_piece)
            if is_valid_column(col, board):
                break
            else:
                print("That column is full! Choose another one.")

        # Drop piece into the board
        row = get_next_open_row(col, board)
        drop_piece(board, row, col, player_piece)

        print_board(board)

        # Check for win
        if winning_move(board, player_piece):
            print(f"Congratulations! Player {player_piece} wins!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw! No more moves possible.")
            break

        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    # Run the game
    main()
