import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5

# Global variables
PLAYERS = ["X", "O", "V", "H", "M"]  # Tokens for players, up to 5 players

def clear_screen():
    """Clears the screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board."""
    # Print column labels
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(col_labels)
    print("+---" * len(board[0]) + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(col, board):
    """Checks if the column is valid and not full."""
    if col < 0 or col >= len(board[0]):  # Check if column is out of bounds
        return False
    return board[0][col] == " "  # Check if there's space in the top row of the column

def drop_checker(col, player, board):
    """Drops a checker into a column."""
    for row in reversed(board):  # Start from the bottom row
        if row[col] == " ":
            row[col] = player
            break

def check_winner(board, player):
    """Checks if the player has won."""
    # Helper function to check 4 in a row
    def check_four_in_a_row(sequence):
        return "".join(sequence).find(player * 4) != -1

    # Check rows
    for row in board:
        if check_four_in_a_row(row):
            return True

    # Check columns
    for col in range(len(board[0])):
        column = [board[row][col] for row in range(len(board))]
        if check_four_in_a_row(column):
            return True

    # Check diagonals (bottom-left to top-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    # Initialize game settings
    board = create_board(ROWS, COLS)
    num_players = 2  # For this assignment, we stick to 2 players
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    # Game loop
    while True:
        clear_screen()
        print_board(board)

        # Ask the current player for their move
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        column = input("Please enter a column (A-G): ").strip().upper()

        # Validate input
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_index = ord(column) - 65  # Convert column letter to index
        if not is_valid_column(col_index, board):
            print("Invalid column. Please choose a different column.")
            continue

        # Place the checker
        drop_checker(col_index, current_player, board)

        # Check for win or draw
        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
