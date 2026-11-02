import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Define player symbols for up to 5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen to keep display clean."""
    os.system('clear')  # Use 'cls' if you are on Windows

def create_board():
    """Create an empty board with ROWS x COLS filled with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    print(' ' + '   '.join(COLUMNS_LABELS))  # Column labels
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print('-' * (COLS * 4 + 1))

def is_valid_column(col_char):
    """Check if the input column character is valid (A-G)."""
    return col_char in COLUMNS_LABELS

def get_column_index(col_char):
    """Convert column character to column index (0-based)."""
    return COLUMNS_LABELS.index(col_char)

def is_column_full(board, col):
    """Check if the specified column is full (no space to drop)."""
    return board[0][col] != ' '

def drop_piece(board, col, piece):
    """
    Drop the player's piece in the specified column.
    Piece falls to the lowest empty row in that column.
    """
    for row in reversed(range(ROWS)):  # Start from bottom
        if board[row][col] == ' ':
            board[row][col] = piece
            return row  # Return the row where piece ended up
    return -1  # Should not happen if checked for full column before

def check_winner(board, row, col, piece):
    """
    Check if placing the piece at (row, col) creates a connect 4.
    We check all directions: vertical, horizontal, two diagonals.
    """
    directions = [
        (1, 0),   # vertical
        (0, 1),   # horizontal
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the dropped piece itself
        
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r += dr
            c += dc
        
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def main():
    print("Welcome to Connect 4!")
    # Ask for number of players (2-5)
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input, enter an integer.")

    # Setup players
    players = PLAYER_SYMBOLS[:num_players]

    # Random first player
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {', '.join(players)}")
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")

        # Input loop for valid column choice
        while True:
            col_input = input(f"Choose a column ({'/'.join(COLUMNS_LABELS)}): ").upper()
            if not is_valid_column(col_input):
                print(f"Invalid column. Choose a letter A-G.")
                continue

            col_idx = get_column_index(col_input)

            if is_column_full(board, col_idx):
                print("That column is full. Choose another one.")
                continue
            
            break

        # Drop the piece in the selected column
        row_placed = drop_piece(board, col_idx, current_player)

        # Check for win
        if check_winner(board, row_placed, col_idx, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
