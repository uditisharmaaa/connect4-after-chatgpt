import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Creates the game board initialized with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column_input, board):
    """Checks if the player input is valid."""
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column_index = ord(column_input.upper()) - 65
    return 0 <= column_index < COLS and board[0][column_index] == " "

def place_checker(board, column_index, player_symbol):
    """Places the player's checker in the specified column."""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player_symbol
            return True
    return False

def check_winner(board, player_symbol):
    """Checks if the specified player has won the game."""
    # Check horizontal, vertical, and diagonal connections
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player_symbol:
                # Check horizontally
                if col + 3 < COLS and all(board[row][col + i] == player_symbol for i in range(4)):
                    return True
                # Check vertically
                if row + 3 < ROWS and all(board[row + i][col] == player_symbol for i in range(4)):
                    return True
                # Check diagonal \
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player_symbol for i in range(4)):
                    return True
                # Check diagonal /
                if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == player_symbol for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the game has ended in a draw (no space left)."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main game function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select starting player
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        column_input = input(f"Player {current_player}, please enter a column: ").strip()

        # Validate input and place checker if valid
        if is_valid_input(column_input, board):
            column_index = ord(column_input.upper()) - 65
            if place_checker(board, column_index, current_player):
                print_board(board)
                # Check for a win
                if check_winner(board, current_player):
                    print(f"Player {current_player} won!")
                    break
                # Check for a draw
                if check_draw(board):
                    print("The game is a draw!")
                    break
                # Switch to the next player
                current_player_index = (current_player_index + 1) % len(PLAYERS)
            else:
                print("Column is full, please choose another column.")
        else:
            print("Invalid input, please enter a letter from A to G.")

if __name__ == "__main__":
    main()
