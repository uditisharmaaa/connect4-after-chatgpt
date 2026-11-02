import os
import random


# Constants for the board dimensions and number of players
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a board filled with whitespaces"""
    return [[' ' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def print_board(board):
    """Prints the board"""
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMN_COUNT)]))
    print("+---" * COLUMN_COUNT + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMN_COUNT + "+")

def is_valid_input(input_char):
    """Checks if the input character is a valid column option"""
    return input_char.isalpha() and 'A' <= input_char < chr(65 + COLUMN_COUNT)

def is_column_full(board, col):
    """Checks if a column is completely filled"""
    return board[0][col] != ' '

def drop_checker(board, col, checker):
    """Drops the checker into the chosen column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    """Checks if the player with the given checker has won"""
    # Check horizontal win
    for row in board:
        for col in range(COLUMN_COUNT - 3):
            if row[col] == checker and all(row[col + offset] == checker for offset in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if board[row][col] == checker and all(board[row + offset][col] == checker for offset in range(4)):
                return True

    # Check diagonal win (positive slope)
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == checker and all(board[row + offset][col + offset] == checker for offset in range(4)):
                return True

    # Check diagonal win (negative slope)
    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == checker and all(board[row - offset][col + offset] == checker for offset in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw"""
    return all(row[0] != ' ' for row in board)

def play_game():
    # Initialize the board
    board = create_board()
    print_board(board)

    # Randomly select starting player
    current_player = random.randint(0, PLAYER_COUNT - 1)

    while True:
        current_checker = CHECKERS[current_player]
        column_input = input(f"Player {current_checker}, please enter a column: ").strip()

        if not is_valid_input(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(column_input) - 65

        if is_column_full(board, column):
            print("Column is full. Please choose another column.")
            continue

        # Drop the checker
        drop_checker(board, column, current_checker)

        # Show the updated board
        print_board(board)

        # Check for win or draw
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYER_COUNT

play_game()
