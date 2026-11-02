import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a game board with specified dimensions initialized to whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def print_board(board):
    """Prints the current state of the board."""
    # Column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def valid_input(column):
    """Check if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 0 <= ord(column) - 65 < COLS

def place_checker(board, column, checker):
    """Place the checker in the selected column if possible, otherwise return False."""
    col_index = ord(column) - 65
    for row in range(ROWS-1, -1, -1):  # Start from bottom row
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check for a win condition for the current player."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is filled, resulting in a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    # Initialize the game
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    game_active = True

    clear_screen()
    print_board(board)

    while game_active:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            column = input().strip().upper()
            if valid_input(column) and place_checker(board, column, current_checker):
                break
            else:
                print(f"Invalid input or column full. Player {current_checker}, please enter a valid column:")

        clear_screen()
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_active = False
        elif check_draw(board):
            print("The game is a draw!")
            game_active = False
        else:
            current_player = (current_player + 1) % PLAYERS  # Switch player

if __name__ == "__main__":
    main()
