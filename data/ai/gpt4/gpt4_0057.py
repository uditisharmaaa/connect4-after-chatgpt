import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Validate user input
def valid_input(input_char, board):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col = ord(input_char.upper()) - 65
    return 0 <= col < COLUMNS and board[0][col] == ' '

# Place checker in the correct column
def place_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

# Check for horizontal win
def check_horizontal(board, checker):
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    return False

# Check for vertical win
def check_vertical(board, checker):
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    return False

# Check for diagonal win (\ direction)
def check_diagonal_1(board, checker):
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for diagonal win (/ direction)
def check_diagonal_2(board, checker):
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check if the board is full (draw)
def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Check for a win or draw condition
def check_winner(board, checker):
    return (check_horizontal(board, checker) or
            check_vertical(board, checker) or
            check_diagonal_1(board, checker) or
            check_diagonal_2(board, checker))

# Main function to run the game
def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select first player
    print_board(board)

    while True:
        print(f"Player {PLAYER_CHECKERS[current_player]}'s turn. Please enter a column (A-{chr(64 + COLUMNS)}):")
        column = input().strip()

        if not valid_input(column, board):
            print("Invalid input! Try again.")
            continue

        place_checker(board, column, PLAYER_CHECKERS[current_player])
        print_board(board)

        # Check for win
        if check_winner(board, PLAYER_CHECKERS[current_player]):
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
