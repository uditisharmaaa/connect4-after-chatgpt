import random
import os

# Constants for board dimensions and player symbols.
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates and returns a 2D board with specified dimensions."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board to the terminal."""
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_valid_column():
    """Prompts the player for a valid column letter input."""
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + COLUMNS - 1):
            return ord(column_input) - ord('A')
        print("Invalid input, please enter a valid column letter.")

def place_checker(board, column, checker):
    """Places the checker in the lowest available spot in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    print("Column is full. Turn lost.")
    return False

def check_for_win(board, checker):
    """Checks the board for a win condition for the specified checker."""
    # Horizontal, vertical and diagonal checks
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4 and all(board[row][col + i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                return True
            if col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    """Checks if the board is completely filled, resulting in a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player_index]}, it's your turn.")
        column = get_valid_column()

        if place_checker(board, column, CHECKERS[current_player_index]):
            print_board(board)

            if check_for_win(board, CHECKERS[current_player_index]):
                print(f"Player {CHECKERS[current_player_index]} won!")
                break

            if check_for_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % PLAYERS

play_game()
