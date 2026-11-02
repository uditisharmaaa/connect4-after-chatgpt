import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board, columns):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * columns + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * columns + "+")


def is_valid_column(column_letter, columns):
    """Check if the column letter is valid."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    column_index = ord(column_letter.upper()) - ord('A')
    return 0 <= column_index < columns


def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, column_index, rows):
    """Check if a checker can be placed in the given column."""
    return board[0][column_index] == " "


def place_checker(board, column_index, checker, rows):
    """Place a checker in the given column and return the row where it was placed."""
    for row in range(rows - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return row
    return -1


def check_direction(board, row, col, checker, drow, dcol, rows, columns):
    """Count consecutive checkers in a given direction."""
    count = 0
    r, c = row + drow, col + dcol
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r += drow
        c += dcol
    return count


def check_win(board, row, col, checker, rows, columns):
    """Check if the last placed checker resulted in a win."""
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for drow, dcol in directions:
        count = 1  # Count the placed checker itself
        
        # Count in positive direction
        count += check_direction(board, row, col, checker, drow, dcol, rows, columns)
        
        # Count in negative direction
        count += check_direction(board, row, col, checker, -drow, -dcol, rows, columns)
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board, rows, columns):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_input(player_checker, columns):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if not is_valid_column(user_input, columns):
            print(f"Invalid input. Please enter a column letter between A and {chr(65 + columns - 1)}.")
            continue
        
        return user_input


def play_game(rows, columns, num_players):
    """Main game loop."""
    board = initialize_board(rows, columns)
    checkers = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board, columns)
    
    while True:
        current_checker = checkers[current_player_index]
        
        # Get valid column from player
        while True:
            column_letter = get_player_input(current_checker, columns)
            column_index = get_column_index(column_letter)
            
            if can_place_checker(board, column_index, rows):
                break
            else:
                print("Column is full. Please choose another column.")
        
        # Place checker and get its row
        placed_row = place_checker(board, column_index, current_checker, rows)
        
        # Print updated board
        print_board(board, columns)
        
        # Check for win
        if check_win(board, placed_row, column_index, current_checker, rows, columns):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, rows, columns):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """Entry point of the program."""
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
