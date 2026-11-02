import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # Extend this list for more players if needed
WINNING_LENGTH = 4

# Function to create and initialize the board
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Function to drop a checker into the board
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Function to check for a win
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - WINNING_LENGTH + 1):
            if all(row[col + i] == checker for i in range(WINNING_LENGTH)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WINNING_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WINNING_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WINNING_LENGTH + 1):
        for col in range(COLUMNS - WINNING_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WINNING_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(WINNING_LENGTH - 1, ROWS):
        for col in range(COLUMNS - WINNING_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WINNING_LENGTH)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)

    while not game_over:
        print(f"Player {current_player}, please enter a column (A to {chr(65 + COLUMNS - 1)}):")
        column_input = input().strip().upper()

        # Validate input
        if len(column_input) != 1 or column_input < 'A' or column_input >= chr(65 + COLUMNS):
            print("Invalid input. Please enter a valid column.")
            continue

        column = ord(column_input) - 65

        if not drop_checker(board, column, current_player):
            print("Column is full. Please select another column.")
            continue

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
