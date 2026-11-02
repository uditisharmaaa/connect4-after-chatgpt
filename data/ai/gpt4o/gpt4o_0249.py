import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

# Initialize the board
def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    column_labels = ' '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+---' * COLUMNS + '+')

# Randomly select a starting player
def get_starting_player(num_players):
    return random.choice(range(num_players))

# Validate column input
def is_valid_input(input_string):
    return len(input_string) == 1 and 'A' <= input_string <= chr(ord('A') + COLUMNS - 1)

# Place a checker in the selected column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Check for a win
def check_winner(board, checker):
    # Horizontal Check
    for row in board:
        if any(checker == row[i] == row[i + 1] == row[i + 2] == row[i + 3] for i in range(COLUMNS - 3)):
            return True

    # Vertical Check
    for col in range(COLUMNS):
        if any(checker == board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] for i in range(ROWS - 3)):
            return True

    # Diagonal (bottom-left to top-right) Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if checker == board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return True

    # Diagonal (top-left to bottom-right) Check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if checker == board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Game loop
def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player = get_starting_player(PLAYERS)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_input(user_input):
            print("Invalid input. Please try again.")
            continue

        column_index = ord(user_input) - ord('A')

        if not place_checker(board, column_index, CHECKERS[current_player]):
            print("Column is full. Please try again.")
            continue

        if check_winner(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
