import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a game board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(i + 65) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col):
    """Checks if the input column is valid."""
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= 'G'

def is_column_full(board, col):
    """Checks if the specified column is full."""
    return board[0][col] != " "

def place_checker(board, col, player):
    """Places a player's checker in the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

def check_win(board, player):
    """Checks if the given player has won the game."""
    # Check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            count = count + 1 if board[r][c] == player else 0
            if count >= 4:
                return True

    # Check vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            count = count + 1 if board[r][c] == player else 0
            if count >= 4:
                return True

    # Check diagonals (/)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True

    # Check diagonals (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        valid_input = False

        while not valid_input:
            col_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()
            if is_valid_input(col_input):
                col = ord(col_input) - 65  # Convert letter to index
                if not is_column_full(board, col):
                    valid_input = True
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a letter between A and G.")

        place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
