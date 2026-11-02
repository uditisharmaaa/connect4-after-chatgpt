import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2  # Change this value for more players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """Creates an empty board with the given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Prints the current state of the board."""
    # Print column headers
    columns = len(board[0])
    print("  " + "   ".join([chr(65 + i) for i in range(columns)]))
    print("+---" * columns + "+")
    
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * columns + "+")


def get_valid_column(board, input_prompt):
    """Validates user input and returns the chosen column index."""
    columns = len(board[0])
    while True:
        try:
            column_input = input(input_prompt).upper()
            if len(column_input) != 1 or not ("A" <= column_input < chr(65 + columns)):
                raise ValueError("Invalid column input. Please enter a valid column letter.")
            
            column_index = ord(column_input) - 65
            if board[0][column_index] != " ":
                raise ValueError("Column is full. Please choose another column.")
            
            return column_index
        except ValueError as e:
            print(e)


def drop_checker(board, column, checker):
    """Places the checker in the lowest available row of the chosen column."""
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            break


def check_winner(board, checker):
    """Checks if the given player has won the game."""
    rows, columns = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(columns - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(columns):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(columns - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(columns - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False


def check_draw(board):
    """Checks if the board is completely filled."""
    return all(board[0][c] != " " for c in range(len(board[0])))


def play_game():
    """Main function to play the Connect 4 game."""
    clear_screen()
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    # Randomly select the starting player
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {CHECKERS[current_player_index]}, it's your turn.")
        
        # Get valid column from current player
        column = get_valid_column(board, "Please enter a column: ")
        
        # Drop the checker in the column
        drop_checker(board, column, CHECKERS[current_player_index])
        
        # Check for win condition
        if check_winner(board, CHECKERS[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player_index]} won!")
            break
        
        # Check for draw condition
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    play_game()
