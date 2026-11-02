import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
MAX_COLS = 26

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display the game board
def display_board(board):
    os.system('clear')  # Clears the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Validate user input
def validate_input(choice, board):
    if len(choice) != 1 or not choice.isalpha():
        return False
    column_index = ord(choice.upper()) - ord('A')
    return 0 <= column_index < COLUMNS and board[0][column_index] == ' '

# Place a checker in the chosen column
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row, column

# Check for win conditions
def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (positive slope) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (negative slope) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for draw (no empty cells)
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
def main():
    board = create_board()
    player_count = PLAYERS
    symbols = CHECKERS[:player_count]
    current_player = random.randint(0, player_count - 1)
    
    display_board(board)
    print(f"Player {symbols[current_player]} starts!")

    while True:
        # Current player's turn
        print(f"Player {symbols[current_player]}, please enter a column: ", end="")
        choice = input().strip().upper()

        # Validate input
        if not validate_input(choice, board):
            print("Invalid input. Try again.")
            continue

        # Place checker and update board
        column_index = ord(choice) - ord('A')
        place_checker(board, column_index, symbols[current_player])
        display_board(board)

        # Check for win
        if check_win(board, symbols[current_player]):
            print(f"Player {symbols[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
