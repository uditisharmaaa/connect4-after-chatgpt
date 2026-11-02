import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    """Clears the terminal screen using 'clear' command."""
    os.system('clear')

def create_board():
    """Creates a blank board with ROWS x COLS filled with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current board state including column labels."""
    print(" " + " ".join(COLUMN_LABELS))  # Print column headers
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))  # Bottom border of board

def get_valid_column_choice(board, player):
    """
    Asks the current player to input a column letter.
    Validates input (letter A-G, column not full).
    Returns the column index (0-6).
    """
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper()
        if choice not in COLUMN_LABELS:
            print("Invalid column. Please select a column letter from A to G.")
            continue
        col = COLUMN_LABELS.index(choice)
        # Check if column is full
        if board[0][col] != ' ':
            print("This column is full. Choose another one.")
            continue
        return col

def drop_piece(board, col, player):
    """
    Drops the player's piece into the chosen column.
    Returns the row index where the piece lands.
    """
    # Start from bottom row upward
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row

def check_direction(board, start_row, start_col, delta_row, delta_col, player):
    """
    Helper function to count consecutive pieces starting at (start_row,start_col)
    moving in direction (delta_row, delta_col).
    Returns count of consecutive player pieces including start cell.
    """
    count = 0
    row, col = start_row, start_col

    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_for_win(board, row, col, player):
    """
    Checks all directions from the last placed piece for 4 in a row.
    Returns True if player wins.
    """
    # Directions: horizontal, vertical, diagonal /
    directions = [
        ((0, 1), (0, -1)),      # Horizontal right and left
        ((1, 0), (-1, 0)),      # Vertical down and up
        ((1, 1), (-1, -1)),     # Diagonal down-right and up-left
        ((1, -1), (-1, 1)),     # Diagonal down-left and up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # Count the current piece
        count += check_direction(board, row + dir1[0], col + dir1[1], dir1[0], dir1[1], player)
        count += check_direction(board, row + dir2[0], col + dir2[1], dir2[0], dir2[1], player)
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Checks if the board is completely filled (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    
    # Get number of players 2 to 5
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input, please enter an integer.")

    players = PLAYER_SYMBOLS[:num_players]

    # Randomly pick starting player
    current_player_index = random.randint(0, num_players -1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]

        # Get valid player move
        col = get_valid_column_choice(board, current_player)

        # Drop the piece in the board
        row = drop_piece(board, col, current_player)

        # Check win
        if check_for_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        # Check draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
