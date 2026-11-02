import os
import random

# Constants for configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
DEFAULT_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
BOARD_CHAR = ' '

# Function to clear the console screen
def clear_screen():
    os.system('clear')  # Use 'cls' instead of 'clear' on Windows

# Function to create the game board
def create_board(rows, columns):
    return [[BOARD_CHAR for _ in range(columns)] for _ in range(rows)]

# Function to print the game board
def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Function to check if the input column is valid
def is_valid_input(column_letter, columns):
    if len(column_letter) != 1:
        return False
    column_index = ord(column_letter.upper()) - 65
    return 0 <= column_index < columns

# Function to drop a checker into the column
def drop_checker(board, column_letter, checker):
    column_index = ord(column_letter.upper()) - 65
    for row in range(len(board) - 1, -1, -1):  # Start from the bottom row
        if board[row][column_index] == BOARD_CHAR:
            board[row][column_index] = checker
            return True
    return False  # Indicates the column is full

# Function to check if a player has won
def check_win(board, checker):
    for row in range(len(board)):
        for column in range(len(board[0])):
            # Check horizontally
            if column <= len(board[0]) - 4 and all(board[row][column + i] == checker for i in range(4)):
                return True
            # Check vertically
            if row <= len(board) - 4 and all(board[row + i][column] == checker for i in range(4)):
                return True
            # Check diagonally (/)
            if row <= len(board) - 4 and column <= len(board[0]) - 4 and all(board[row + i][column + i] == checker for i in range(4)):
                return True
            # Check diagonally (\)
            if row >= 3 and column <= len(board[0]) - 4 and all(board[row - i][column + i] == checker for i in range(4)):
                return True
    return False

# Function to check if the game is a draw
def check_draw(board):
    return all(board[0][column] != BOARD_CHAR for column in range(len(board[0])))

# Main function to run the Connect 4 game
def connect_4_game():
    board = create_board(ROWS, COLUMNS)
    players = DEFAULT_PLAYERS
    checkers = CHECKERS[:players]
    current_player_index = random.choice(range(players))

    print_board(board)

    while True:
        current_checker = checkers[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        column_choice = input().strip()

        if not is_valid_input(column_choice, COLUMNS):
            print("Invalid input. Please enter a valid column letter.")
            continue

        if not drop_checker(board, column_choice, current_checker):
            print("The column is full, you lose your turn.")
            current_player_index = (current_player_index + 1) % players
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % players

# Run the game
if __name__ == "__main__":
    connect_4_game()
