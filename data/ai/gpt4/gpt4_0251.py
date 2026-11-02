import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Creates an empty board with specified dimensions."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Displays the board in the required format."""
    os.system('clear')  # Clear the terminal screen
    # Print column headers
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_index(column_char):
    """Converts column letter to an index (A -> 0, B -> 1, etc.)."""
    return ord(column_char.upper()) - 65

def is_valid_column(column_char, board):
    """Checks if the input column is valid and not full."""
    if len(column_char) != 1 or not column_char.isalpha():
        return False
    col_index = get_column_index(column_char)
    if col_index < 0 or col_index >= COLUMNS:
        return False
    return board[0][col_index] == " "  # Check if the column is not full

def drop_checker(board, column_char, checker):
    """Drops the checker in the chosen column."""
    col_index = get_column_index(column_char)
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index  # Return the position of the placed checker

def check_win(board, row, col, checker):
    """Checks for a win condition horizontally, vertically, or diagonally."""
    def count_in_direction(delta_row, delta_col):
        """Counts checkers in a specific direction."""
        r, c = row, col
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check all directions: horizontal, vertical, and both diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = count_in_direction(dr, dc) + count_in_direction(-dr, -dc) - 1
        if total >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the board is full and it is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    """Main function to play the Connect 4 game."""
    # Initialization
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]  # Select checkers for players
    current_player = random.choice(players)          # Randomly select starting player
    print("Welcome to Connect 4!")
    print_board(board)

    while True:
        print(f"Player {current_player}, it's your turn!")
        while True:
            column = input("Please enter a column (A-G): ").strip()
            if is_valid_column(column, board):
                break
            print("Invalid input. Please try again.")

        # Drop checker and update the board
        row, col = drop_checker(board, column, current_player)
        print_board(board)

        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % PLAYERS]

if __name__ == "__main__":
    play_game()
