import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum of 5 players
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # Generate column labels A-G

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board to the terminal
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(COLUMN_LABELS))  # Column headers
    print("+---" * COLUMNS + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")  # Row border

# Drop a checker into the desired column
def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check if the board is full
def check_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

# Validate user input for a column
def validate_input(column_input):
    return column_input in COLUMN_LABELS

# Main game logic
def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    player_symbols = CHECKERS[:PLAYERS]
    game_over = False

    print_board(board)
    print(f"Player {player_symbols[current_player]} goes first!")

    while not game_over:
        # Get the current player's turn
        player_symbol = player_symbols[current_player]
        move_valid = False

        # Prompt for valid input
        while not move_valid:
            column_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
            if validate_input(column_input):
                column_index = COLUMN_LABELS.index(column_input)
                if drop_checker(board, column_index, player_symbol):
                    move_valid = True
                else:
                    print(f"Column {column_input} is full. Choose another column.")
            else:
                print(f"Invalid input. Please enter a valid column (A-{chr(64 + COLUMNS)}).")
        
        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            game_over = True
            continue

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            continue

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
