import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """Create and initialize the board with empty spaces."""
    board = []
    for row in range(rows):
        new_row = []
        for col in range(columns):
            new_row.append(" ")
        board.append(new_row)
    return board


def print_board(board, columns):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with separators
    for row in board:
        print("+---" * columns + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * columns + "+")


def is_valid_column(column_input, columns):
    """Check if the column input is valid."""
    if len(column_input) != 1:
        return False
    
    if not column_input.isalpha():
        return False
    
    column_letter = column_input.upper()
    column_index = ord(column_letter) - ord('A')
    
    if column_index < 0 or column_index >= columns:
        return False
    
    return True


def get_column_index(column_input):
    """Convert column letter to index."""
    return ord(column_input.upper()) - ord('A')


def is_column_full(board, column_index):
    """Check if a column is completely full."""
    return board[0][column_index] != " "


def place_checker(board, column_index, checker):
    """Place a checker in the lowest available position of a column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True
    return False


def check_horizontal_win(board, rows, columns, checker):
    """Check if there is a horizontal win for the given checker."""
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, columns, checker):
    """Check if there is a vertical win for the given checker."""
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, rows, columns, checker):
    """Check if there is a diagonal win for the given checker."""
    # Check diagonals going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, rows, columns, checker):
    """Check if the given checker has won."""
    if check_horizontal_win(board, rows, columns, checker):
        return True
    if check_vertical_win(board, rows, columns, checker):
        return True
    if check_diagonal_win(board, rows, columns, checker):
        return True
    return False


def is_board_full(board, rows, columns):
    """Check if the board is completely full (draw condition)."""
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get checkers for each player
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Choose random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = player_checkers[current_player_index]
        player_number = current_player_index + 1
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            
            if not is_valid_column(column_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column_index = get_column_index(column_input)
            
            if is_column_full(board, column_index):
                print("This column is full. Please choose another column.")
                continue
            
            # Valid input received
            break
        
        # Place checker
        place_checker(board, column_index, current_checker)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, ROWS, COLUMNS, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Main program
if __name__ == "__main__":
    play_game()
