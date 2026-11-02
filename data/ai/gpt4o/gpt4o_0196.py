import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5  # This can be 2 to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the game board screen."""
    os.system('clear')

def print_board(board):
    """Prints the current game board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("|" + "   |" * COLUMNS)
        print("|" + " ".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * COLUMNS)

def create_board(rows, columns):
    """Creates a board initialized with spaces."""
    return [[" "] * columns for _ in range(rows)]

def is_valid_input(input_char, board):
    """Checks if the input is a valid column letter and not full."""
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    column_index = ord(input_char.upper()) - 65
    if 0 <= column_index < COLUMNS:
        return board[0][column_index] == " "
    return False

def place_checker(board, column_index, checker):
    """Places the checker in the lowest available spot in the column."""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

def check_winner(board, checker):
    """Checks for 4 in a row: horizontally, vertically, or diagonally."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                # Check horizontally
                if col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertically
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal downwards
                if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal upwards
                if row - 3 >= 0 and col + 3 < COLUMNS and all(board[row - i][col + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the board is completely filled resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    # Supports 2 players for submission, could be set to any valid value with MAX_PLAYERS.
    num_players = 2
    checkers = CHECKERS[:num_players]
    # Randomly select the first player
    current_player = random.choice(range(num_players))

    print("Welcome to Connect 4!")

    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column:")
        player_input = input().strip().upper()

        if not is_valid_input(player_input, board):
            print("Invalid input, please enter a valid column letter.")
            continue

        column_index = ord(player_input) - 65
        place_checker(board, column_index, checkers[current_player])
        
        if check_winner(board, checkers[current_player]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
