import random
import os

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Assuming at max 5 players

def create_board():
    """Initializes a board with whitespaces."""
    return [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Prints the board."""
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(NUM_COLUMNS)]))
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

def get_player_input(current_player):
    """Gets and validates the player's input."""
    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if column.isalpha() and len(column) == 1:
            column_index = ord(column) - 65
            if 0 <= column_index < NUM_COLUMNS:
                return column_index
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column_index, checker):
    """Places the checker into the desired column."""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    print(f"Column {chr(65 + column_index)} is full. You lose your turn.")
    return False

def check_win(board, checker):
    """Checks if there's a win condition in the board."""
    # Horizontal check
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if all(cell == checker for cell in row[col:col+4]):
                return True
    # Vertical check
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Diagonal checks
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            # Check for positive slope
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
            # Check for negative slope
            if all(board[row+3-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the board is full, resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def connect_4_game():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Random start
    print_board(board)

    while True:
        column_index = get_player_input(current_player)
        if place_checker(board, column_index, CHECKERS[current_player]):
            print_board(board)
            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_4_game()
