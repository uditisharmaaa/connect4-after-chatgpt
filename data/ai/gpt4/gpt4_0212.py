import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the screen."""
    os.system('clear')

def create_board():
    """Create a 2D game board initialized with spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board state."""
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(board, col):
    """Check if the column is valid and not full."""
    return 0 <= col < COLUMNS and board[0][col] == " "

def get_column_from_input(board):
    """Get a valid column index from the player."""
    while True:
        user_input = input("Please enter a column (A-G): ").strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLUMNS - 1):
            col = ord(user_input) - 65
            if is_valid_column(board, col):
                return col
            else:
                print(f"Column {user_input} is full. Try again.")
        else:
            print("Invalid input. Enter a letter in the range A-G.")

def drop_checker(board, col, symbol):
    """Drop the checker into the lowest empty row of a column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row

def check_winner(board, row, col, symbol):
    """Check if the current player won after their move."""
    def count_consecutive(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        return count

    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]

    for delta_row, delta_col in directions:
        if count_consecutive(delta_row, delta_col) + count_consecutive(-delta_row, -delta_col) + 1 >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def connect_4():
    """Main function to play the Connect 4 game."""
    # Initialize game
    board = create_board()
    num_players = 2  # Only support 2 players for now
    players = PLAYER_SYMBOLS[:num_players]
    random.shuffle(players)
    
    current_player_index = 0
    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    while True:
        # Current player's turn
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        col = get_column_from_input(board)
        row = drop_checker(board, col, current_player)
        
        print_board(board)

        # Check for win or draw
        if check_winner(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    connect_4()
