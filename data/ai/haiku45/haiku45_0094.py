import os
import random

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def create_board(rows, columns):
    """Create and initialize the board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(" ")
        board.append(row)
    return board


def print_board(board, columns):
    """Print the board in a formatted way."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(columns):
        print(chr(ord('A') + i), end="   ")
    print()
    
    # Print top border
    print("+---" * columns + "+")
    
    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * columns + "+")


def is_valid_input(user_input, columns):
    """Check if the user input is valid."""
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if input is uppercase letter
    if not user_input.isupper():
        return False
    
    # Check if input is a letter
    if not user_input.isalpha():
        return False
    
    # Check if column is within board range
    column_index = ord(user_input) - ord('A')
    if column_index < 0 or column_index >= columns:
        return False
    
    return True


def get_column_input(player_checker, columns):
    """Get valid column input from player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        if is_valid_input(user_input, columns):
            return ord(user_input) - ord('A')
        print("Invalid input. Please enter a valid column letter.")


def can_place_checker(board, column, rows):
    """Check if a checker can be placed in the given column."""
    # Check if column is not completely filled
    if board[0][column] != " ":
        return False
    return True


def place_checker(board, column, checker, rows):
    """Place a checker in the given column and return the row where it was placed."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row
    return -1


def check_horizontal_win(board, row, column, checker, columns):
    """Check if there is a horizontal win starting from the given position."""
    count = 0
    
    # Check to the left and right
    for col in range(columns):
        if board[row][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_vertical_win(board, row, column, checker, rows):
    """Check if there is a vertical win starting from the given position."""
    count = 0
    
    # Check upward and downward
    for r in range(rows):
        if board[r][column] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_diagonal_win_right(board, row, column, checker, rows, columns):
    """Check for diagonal win going down-right and up-left."""
    count = 0
    
    # Check all diagonal positions
    for i in range(max(rows, columns)):
        r = row - column + i
        c = i
        
        if r < 0 or r >= rows or c < 0 or c >= columns:
            if count >= WIN_LENGTH:
                return True
            count = 0
            continue
        
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_diagonal_win_left(board, row, column, checker, rows, columns):
    """Check for diagonal win going down-left and up-right."""
    count = 0
    
    # Check all diagonal positions
    for i in range(max(rows, columns)):
        r = row + column - i
        c = i
        
        if r < 0 or r >= rows or c < 0 or c >= columns:
            if count >= WIN_LENGTH:
                return True
            count = 0
            continue
        
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_win(board, row, column, checker, rows, columns):
    """Check if the current move results in a win."""
    # Check horizontal
    if check_horizontal_win(board, row, column, checker, columns):
        return True
    
    # Check vertical
    if check_vertical_win(board, row, column, checker, rows):
        return True
    
    # Check diagonal (right direction)
    if check_diagonal_win_right(board, row, column, checker, rows, columns):
        return True
    
    # Check diagonal (left direction)
    if check_diagonal_win_left(board, row, column, checker, rows, columns):
        return True
    
    return False


def is_board_full(board, rows, columns):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True


def play_game(board, rows, columns, num_players):
    """Main game loop."""
    checkers = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, columns)
    
    while True:
        current_checker = checkers[current_player_index]
        
        # Get player input
        while True:
            column = get_column_input(current_checker, columns)
            
            # Check if checker can be placed
            if can_place_checker(board, column, rows):
                row = place_checker(board, column, current_checker, rows)
                break
            else:
                print("Column is full. Please choose another column.")
        
        # Print updated board
        print_board(board, columns)
        
        # Check for win
        if check_win(board, row, column, current_checker, rows, columns):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, rows, columns):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """Initialize and start the game."""
    board = create_board(NUM_ROWS, NUM_COLUMNS)
    play_game(board, NUM_ROWS, NUM_COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
