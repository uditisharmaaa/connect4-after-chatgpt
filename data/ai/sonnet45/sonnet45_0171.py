import random
import os

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print rows with dividers
    for row in range(ROWS):
        # Print top border
        print('  +', end='')
        for col in range(COLS):
            print('---+', end='')
        print()
        
        # Print row content
        print('  |', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print('  +', end='')
    for col in range(COLS):
        print('---+', end='')
    print()


def is_valid_input(column_input, board):
    """Check if the input is valid and the column is not full."""
    # Check if input is a single character
    if len(column_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not column_input.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(column_input) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False
    
    return True


def place_checker(board, column_input, checker):
    """Place the checker in the specified column and return the row position."""
    col_index = ord(column_input) - 65
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, checker, -1, 1):
        return True
    
    return False


def check_direction(board, row, col, checker, row_delta, col_delta):
    """Check if there are 4 checkers in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    count += count_consecutive(board, row, col, checker, row_delta, col_delta)
    
    # Check in negative direction
    count += count_consecutive(board, row, col, checker, -row_delta, -col_delta)
    
    return count >= WIN_LENGTH


def count_consecutive(board, row, col, checker, row_delta, col_delta):
    """Count consecutive checkers in a specific direction."""
    count = 0
    current_row = row + row_delta
    current_col = col + col_delta
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == checker):
        count += 1
        current_row += row_delta
        current_col += col_delta
    
    return count


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def main():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Create list of players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid input from the current player
        valid_input = False
        while not valid_input:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            
            if is_valid_input(column_input, board):
                valid_input = True
            else:
                print("Invalid input. Please try again.")
        
        # Place the checker
        row = place_checker(board, column_input, current_checker)
        col = ord(column_input) - 65
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
