import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "
WIN_COUNT = 4

# Function to clear the screen
def clear_screen():
    os.system('clear')

# Function to initialize the board
def initialize_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

# Function to print the board to the screen
def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(NUM_COLS)))
    print("+---" * NUM_COLS + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

# Function to get the lowest available row in a column
def get_available_row(board, col):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row
    return -1

# Function to check if the input column is valid
def is_valid_column(column_input, columns_filled):
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column_index = ord(column_input.upper()) - ord('A')
    return 0 <= column_index < NUM_COLS and columns_filled[column_index] < NUM_ROWS

# Function to place a checker in the board
def place_checker(board, col, checker):
    row = get_available_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

# Function to check for a win
def check_win(board, checker):
    # Horizontal check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_COUNT + 1):
            if all(board[row][col + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - WIN_COUNT + 1):
            if all(board[row + i][col] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (bottom-left to top-right) check
    for row in range(NUM_ROWS - WIN_COUNT + 1):
        for col in range(NUM_COLS - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right) check
    for row in range(WIN_COUNT - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

# Function to check for a draw (board full)
def check_draw(columns_filled):
    return all(fill == NUM_ROWS for fill in columns_filled)

# Main function
def main():
    # Initialize board and variables
    board = initialize_board(NUM_ROWS, NUM_COLS)
    columns_filled = [0] * NUM_COLS  # Keeps track of how many checkers are in each column
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Randomly select first player
    game_over = False

    print_board(board)
    print(f"Player {players[current_player_index]} starts the game!")

    while not game_over:
        current_player = players[current_player_index]
        column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if not is_valid_column(column_input, columns_filled):
            print("Invalid input. Please enter a valid column.")
            continue

        column_index = ord(column_input) - ord('A')
        if place_checker(board, column_index, current_player):
            columns_filled[column_index] += 1
            print_board(board)

            # Check for win or draw
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(columns_filled):
                print("The game is a draw!")
                game_over = True
            else:
                # Switch turns
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {column_input} is full. Try another column.")

if __name__ == "__main__":
    main()
