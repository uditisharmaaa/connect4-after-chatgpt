import os
import random

# Global constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create a board with dimensions ROWS x COLUMNS and initialize with whitespace."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(col + ord('A')) for col in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_value):
    """Checks if the input is valid (an uppercase letter within the column range)."""
    if len(input_value) == 1 and input_value.isalpha():
        col_index = ord(input_value.upper()) - ord('A')
        return 0 <= col_index < COLUMNS
    return False

def get_column_index(column_letter):
    """Get the column index from the column letter."""
    return ord(column_letter.upper()) - ord('A')

def get_empty_row(board, col_index):
    """Find the first empty row in the given column."""
    for row_index in range(ROWS-1, -1, -1):
        if board[row_index][col_index] == " ":
            return row_index
    return None

def place_checker(board, player, col_index):
    """Place the player's checker in the given column, if possible."""
    row_index = get_empty_row(board, col_index)
    if row_index is not None:
        board[row_index][col_index] = player
        return True
    return False

def check_win(board, player):
    """Check if the given player has won the game."""
    # Check horizontally
    for row in board:
        for col_index in range(COLUMNS - 3):
            if all(row[col_index + offset] == player for offset in range(4)):
                return True

    # Check vertically
    for col_index in range(COLUMNS):
        for row_index in range(ROWS - 3):
            if all(board[row_index + offset][col_index] == player for offset in range(4)):
                return True

    # Check positively sloped diagonals
    for row_index in range(ROWS - 3):
        for col_index in range(COLUMNS - 3):
            if all(board[row_index + offset][col_index + offset] == player for offset in range(4)):
                return True

    # Check negatively sloped diagonals
    for row_index in range(3, ROWS):
        for col_index in range(COLUMNS - 3):
            if all(board[row_index - offset][col_index + offset] == player for offset in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is completely filled resulting in a draw."""
    return all(board[0][col_index] != " " for col_index in range(COLUMNS))

def connect_4_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(CHECKERS[:PLAYERS])
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        player_input = input().strip()
        
        while not is_valid_input(player_input):
            print("Invalid input! Please enter a valid column:")
            player_input = input().strip()

        col_index = get_column_index(player_input)
        if place_checker(board, current_player, col_index):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            
            # Alternate turn to next player
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column full! Turn lost.")

if __name__ == "__main__":
    connect_4_game()
