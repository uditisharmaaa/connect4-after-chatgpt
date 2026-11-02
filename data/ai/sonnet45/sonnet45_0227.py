import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print(' ', end=' ')
    for col in range(COLS):
        print(f' {chr(65 + col)} ', end=' ')
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print('+' + '---+' * COLS)
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print('+' + '---+' * COLS)


def is_valid_column(col_letter, board):
    """Check if the column input is valid and not full."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False, "Invalid input. Please enter a single column letter."
    
    # Check if input is a letter
    if not col_letter.isalpha():
        return False, "Invalid input. Please enter a letter."
    
    # Convert to uppercase and get column index
    col_letter = col_letter.upper()
    col_index = ord(col_letter) - ord('A')
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False, f"Invalid column. Please choose between A and {chr(65 + COLS - 1)}."
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False, "Column is full. Please choose another column."
    
    return True, col_index


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available position."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
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


def check_direction(board, row, col, checker, delta_row, delta_col):
    """Check if there are 4 checkers in a row in a specific direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    count += count_consecutive(board, row, col, checker, delta_row, delta_col)
    
    # Check in negative direction
    count += count_consecutive(board, row, col, checker, -delta_row, -delta_col)
    
    return count >= WIN_LENGTH


def count_consecutive(board, row, col, checker, delta_row, delta_col):
    """Count consecutive checkers in a given direction."""
    count = 0
    current_row = row + delta_row
    current_col = col + delta_col
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLS and 
           board[current_row][current_col] == checker):
        count += 1
        current_row += delta_row
        current_col += delta_col
    
    return count


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def play_game():
    """Main game loop."""
    # Initialize game
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get valid input from player
        while True:
            col_input = input(f"Player {current_checker}, please enter a column: ")
            valid, result = is_valid_column(col_input, board)
            
            if valid:
                col_index = result
                break
            else:
                print(result)
        
        # Place checker
        row = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
