import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board():
    """Create and return a board with all cells initialized to whitespace."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print('  ', end='')
    for col in range(COLS):
        print(f'{chr(65 + col)}   ', end='')
    print()
    
    # Print board with rows
    for row in range(ROWS):
        print('+---' * COLS + '+')
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    print('+---' * COLS + '+')


def is_valid_column(column_letter):
    """Check if the column input is valid."""
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isalpha():
        return False
    
    col_index = ord(column_letter.upper()) - 65
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    return True


def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter.upper()) - 65


def can_place_checker(board, col_index):
    """Check if a checker can be placed in the given column."""
    if col_index < 0 or col_index >= COLS:
        return False
    
    return board[0][col_index] == ' '


def place_checker(board, col_index, checker):
    """Place a checker in the given column and return the row where it was placed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """Check if the placed checker results in a win."""
    # Check horizontal
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Check top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    # Check bottom-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Check bottom-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!")
    input("Press Enter to continue...")
    
    game_over = False
    
    while not game_over:
        print_board(board)
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip()
            
            if not is_valid_column(column_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = get_column_index(column_input)
            
            if not can_place_checker(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place checker
        row = place_checker(board, col_index, CHECKERS[current_player])
        
        # Check for win
        if check_win(board, row, col_index, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        if not game_over:
            current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
