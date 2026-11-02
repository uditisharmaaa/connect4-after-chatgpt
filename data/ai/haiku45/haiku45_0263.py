import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, columns):
    """Initialize the board with all empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def get_column_letter(index):
    """Convert column index to letter (0 -> A, 1 -> B, etc.)."""
    return chr(ord('A') + index)


def print_board(board, rows, columns):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(f" {get_column_letter(col)}  ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(columns):
        print("---+", end="")
    print()
    
    # Print rows
    for row in range(rows):
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
        print("+", end="")
        for col in range(columns):
            print("---+", end="")
        print()


def is_valid_column_input(column_input, columns):
    """Validate if the input is a valid column."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    column_input = column_input.upper()
    col_index = ord(column_input) - ord('A')
    return 0 <= col_index < columns


def get_column_index(column_input):
    """Convert column letter to index."""
    return ord(column_input.upper()) - ord('A')


def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker, rows):
    """Place a checker in the specified column."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_horizontal_win(board, rows, columns, checker):
    """Check if there's a horizontal win for the given checker."""
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, columns, checker):
    """Check if there's a vertical win for the given checker."""
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_right_win(board, rows, columns, checker):
    """Check if there's a diagonal win (top-left to bottom-right) for the given checker."""
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_left_win(board, rows, columns, checker):
    """Check if there's a diagonal win (top-right to bottom-left) for the given checker."""
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_win(board, rows, columns, checker):
    """Check if the current player has won."""
    return (check_horizontal_win(board, rows, columns, checker) or
            check_vertical_win(board, rows, columns, checker) or
            check_diagonal_right_win(board, rows, columns, checker) or
            check_diagonal_left_win(board, rows, columns, checker))


def is_board_full(board, rows, columns):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True


def get_valid_column_input(columns):
    """Get a valid column input from the player."""
    while True:
        user_input = input("Please enter a column (A-" + get_column_letter(columns - 1) + "): ")
        if is_valid_column_input(user_input, columns):
            return get_column_index(user_input)
        print("Invalid input. Please enter a valid column.")


def play_game(rows, columns, num_players):
    """Main game loop."""
    board = initialize_board(rows, columns)
    checkers = CHECKERS[:num_players]
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, rows, columns)
    
    # Game loop
    while True:
        current_checker = checkers[current_player_index]
        player_name = chr(ord('1') + current_player_index) if num_players > 2 else current_checker
        
        # Get valid column input
        while True:
            print(f"Player {current_checker}, please enter a column:")
            col_index = get_valid_column_input(columns)
            
            # Check if column is full
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            # Place the checker
            place_checker(board, col_index, current_checker, rows)
            break
        
        # Print the board
        print_board(board, rows, columns)
        
        # Check for win
        if check_win(board, rows, columns, current_checker):
            print(f"Player {current_checker} won!")
            return
        
        # Check for draw
        if is_board_full(board, rows, columns):
            print("It's a draw!")
            return
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """Main function to start the game."""
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
