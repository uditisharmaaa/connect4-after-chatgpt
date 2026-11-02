import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Initialize the board with blank spaces
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Clear the screen and print the board
def print_board(board):
    os.system('clear')
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Get valid column input from player
def get_column_input():
    while True:
        letter = input("Please enter a column: ").upper()
        if letter.isalpha() and 'A' <= letter <= chr(ord('A') + COLUMNS - 1):
            return ord(letter) - ord('A')
        print("Invalid input. Try again.")

# Place checker in the lowest available row in the chosen column
def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False  # Column is full

# Check for a win condition in the board
def check_for_win(board, symbol):
    def check_direction(x, y, dx, dy):
        count = 0
        for _ in range(4):
            if 0 <= x < ROWS and 0 <= y < COLUMNS and board[x][y] == symbol:
                count += 1
            x, y = x + dx, y + dy
        return count == 4

    for x in range(ROWS):
        for y in range(COLUMNS):
            if board[x][y] == symbol:
                if (check_direction(x, y, 1, 0) or  # Vertical
                    check_direction(x, y, 0, 1) or  # Horizontal
                    check_direction(x, y, 1, 1) or  # Diagonal \
                    check_direction(x, y, 1, -1)):  # Diagonal /
                    return True
    return False

# Check for a draw condition
def check_for_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main function to handle game logic
def main():
    # Create and print initial board
    board = create_board()
    print_board(board)

    # Set the game with 2 players
    num_players = 2
    player_symbols = PLAYER_SYMBOLS[:num_players]

    # Randomly select first player
    current_player = random.choice(range(num_players))

    while True:
        symbol = player_symbols[current_player]
        print(f"Player {symbol}, it's your turn.")

        # Get column input and try to place checker
        column = get_column_input()
        if not place_checker(board, column, symbol):
            print("Column is full. Turn lost.")
        else:
            print_board(board)

            # Check for win condition
            if check_for_win(board, symbol):
                print(f"Player {symbol} wins!")
                break

            # Check for draw condition
            if check_for_draw(board):
                print("The game is a draw!")
                break

            # Switch to next player
            current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
