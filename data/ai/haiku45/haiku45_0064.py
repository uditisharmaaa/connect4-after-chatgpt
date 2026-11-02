import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create and initialize the board with empty spaces."""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()


def is_valid_input(user_input, cols):
    """Validate user input for column selection."""
    if len(user_input) != 1:
        return False
    
    col_letter = user_input.upper()
    
    if not col_letter.isalpha():
        return False
    
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_index(user_input):
    """Convert column letter to column index."""
    return ord(user_input.upper()) - ord('A')


def can_place_checker(board, col_index, rows):
    """Check if a checker can be placed in the given column."""
    if board[0][col_index] == " ":
        return True
    return False


def place_checker(board, col_index, checker, rows):
    """Place a checker in the given column and return the row index."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_horizontal_win(board, row, col, checker, cols):
    """Check if there are 4 checkers in a row horizontally."""
    count = 0
    
    # Check all horizontal positions
    for c in range(cols):
        if board[row][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_vertical_win(board, row, col, checker, rows):
    """Check if there are 4 checkers in a row vertically."""
    count = 0
    
    # Check all vertical positions
    for r in range(rows):
        if board[r][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_diagonal_win(board, row, col, checker, rows, cols):
    """Check if there are 4 checkers in a row diagonally."""
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    r, c = row, col
    # Move to the start of the diagonal
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    # Count checkers along this diagonal
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-right to bottom-left)
    count = 0
    r, c = row, col
    # Move to the start of the diagonal
    while r > 0 and c < cols - 1:
        r -= 1
        c += 1
    # Count checkers along this diagonal
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False


def is_win(board, row, col, checker, rows, cols):
    """Check if the last move resulted in a win."""
    if check_horizontal_win(board, row, col, checker, cols):
        return True
    if check_vertical_win(board, row, col, checker, rows):
        return True
    if check_diagonal_win(board, row, col, checker, rows, cols):
        return True
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game(rows, cols, num_players):
    """Main game loop."""
    board = create_board(rows, cols)
    checkers = CHECKERS[:num_players]
    
    # Randomly select first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    
    game_over = False
    
    while not game_over:
        current_checker = checkers[current_player_index]
        player_number = current_player_index + 1
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            
            if not is_valid_input(user_input, cols):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = get_column_index(user_input)
            
            if not can_place_checker(board, col_index, rows):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row_index = place_checker(board, col_index, current_checker, rows)
        
        # Print updated board
        print_board(board, cols)
        
        # Check for win
        if is_win(board, row_index, col_index, current_checker, rows, cols):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, rows, cols):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % num_players


def main():
    """Initialize and start the game."""
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
