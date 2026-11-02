import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal."""
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(input_column, columns):
    """Checks if the input column is valid."""
    return len(input_column) == 1 and input_column.isalpha() and 'A' <= input_column <= chr(65 + columns - 1)

def is_column_full(board, col):
    """Checks if a column is full."""
    return board[0][col] != " "

def place_checker(board, column, symbol):
    """Places the player's checker in the chosen column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return row, column

def check_winner(board, row, col, symbol):
    """Checks for a win condition starting from the position (row, col)."""
    directions = [
        [(0, 1), (0, -1)],   # Horizontal
        [(1, 0), (-1, 0)],   # Vertical
        [(1, 1), (-1, -1)],  # Diagonal /
        [(1, -1), (-1, 1)]   # Diagonal \
    ]

    for direction in directions:
        count = 1  # Include the current position
        for d in direction:
            r, c = row, col
            while True:
                r += d[0]
                c += d[1]
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    for col in range(len(board[0])):
        if not is_column_full(board, col):
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    # Game setup
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed at 2 for this assignment
    player_symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)  # Select random player to start

    print_board(board)
    print(f"Player {player_symbols[current_player]} goes first!")

    # Game loop
    while True:
        # Ask the current player for their move
        player_symbol = player_symbols[current_player]
        while True:
            input_column = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
            if is_valid_input(input_column, COLUMNS):
                column = ord(input_column) - 65
                if not is_column_full(board, column):
                    break
                else:
                    print("Column is full! Please choose a different column.")
            else:
                print("Invalid input! Please enter a valid column letter.")

        # Place the checker and print the board
        row, col = place_checker(board, column, player_symbol)
        print_board(board)

        # Check for a win
        if check_winner(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
