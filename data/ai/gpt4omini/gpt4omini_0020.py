import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Creates and returns a new game board initialized with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col_input):
    """Checks if user input is valid."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_index = ord(col_input.upper()) - 65
    return 0 <= col_index < COLS

def get_column_index(col_input):
    """Converts a column input letter (A-G) to a column index (0-6)."""
    return ord(col_input.upper()) - 65

def drop_checker(board, col_index, checker):
    """Places the checker in the specified column."""
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal, vertical and diagonal lines
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)) or  # Horizontal
                r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)) or  # Vertical
                c <= COLS - 4 and r <= ROWS - 4 and all(board[r + i][c + i] == checker for i in range(4)) or  # Diagonal \
                c >= 3 and r <= ROWS - 4 and all(board[r + i][c - i] == checker for i in range(4))):  # Diagonal /
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player_index = random.randint(0, 1)  # Start with a random player
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        valid_move = False

        while not valid_move:
            col_input = input(f"Player {current_player}, please enter a column (A-G): ").strip()
            if is_valid_input(col_input):
                col_index = get_column_index(col_input)
                valid_move = drop_checker(board, col_index, current_player)
                if not valid_move:
                    print("Column is full! Please try again.")
            else:
                print("Invalid input! Please enter a letter (A-G).")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch player

if __name__ == "__main__":
    main()
