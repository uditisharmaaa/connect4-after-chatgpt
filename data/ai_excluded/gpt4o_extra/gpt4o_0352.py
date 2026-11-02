import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Clear the screen and print the board
def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if the input column is valid and has space
def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

# Place checker in the correct row in the specified column
def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            break

# Check for a winner
def check_winner(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == symbol for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for cell in board[0])

# Main game loop
def main():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)

    while True:
        print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")
        
        while True:
            player_input = input().upper().strip()

            if len(player_input) == 1 and player_input.isalpha():
                column = ord(player_input) - ord('A')
                if is_valid_column(column, board):
                    place_checker(board, column, PLAYER_SYMBOLS[current_player])
                    break
                else:
                    print("Invalid input or column full. Try again.")
            else:
                print("Invalid input. Please enter a valid column letter.")

        print_board(board)

        if check_winner(board, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
