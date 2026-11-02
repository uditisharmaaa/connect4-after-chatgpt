import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return a board with all cells initialized to spaces."""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_column(col_letter):
    """Check if the input is a valid column letter."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_index = ord(col_letter.upper()) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True


def get_column_index(col_letter):
    """Convert column letter to column index."""
    return ord(col_letter.upper()) - 65


def can_place_checker(board, col_index):
    """Check if a checker can be placed in the given column."""
    if board[0][col_index] == " ":
        return True
    return False


def place_checker(board, col_index, checker):
    """Place a checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_horizontal_win(board, row, col, checker):
    """Check if there's a horizontal win at the given position."""
    count = 0
    # Check left
    for c in range(col, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Check right (excluding the current cell to avoid double counting)
    for c in range(col + 1, COLS):
        if board[row][c] == checker:
            count += 1
        else:
            break
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there's a vertical win at the given position."""
    count = 0
    # Check down
    for r in range(row, ROWS):
        if board[r][col] == checker:
            count += 1
        else:
            break
    # Check up (excluding the current cell to avoid double counting)
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    return count >= WIN_LENGTH


def check_diagonal_win_lr(board, row, col, checker):
    """Check for diagonal win (top-left to bottom-right)."""
    count = 0
    # Check up-left
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c -= 1
    # Check down-right (excluding current cell)
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c += 1
    return count >= WIN_LENGTH


def check_diagonal_win_rl(board, row, col, checker):
    """Check for diagonal win (top-right to bottom-left)."""
    count = 0
    # Check up-right
    r, c = row, col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c += 1
    # Check down-left (excluding current cell)
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c -= 1
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win_lr(board, row, col, checker):
        return True
    if check_diagonal_win_rl(board, row, col, checker):
        return True
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print()
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        current_player_name = chr(65 + current_player_index) if current_player_index > 0 else current_checker
        
        # Get valid input from player
        while True:
            col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + COLS - 1)))
                continue
            
            col_index = get_column_index(col_input)
            
            if not can_place_checker(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        row = place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        print()
        
        # Check for win
        if check_win(board, row, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
