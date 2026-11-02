import os
import random

# Game configuration constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column(col_input, cols):
    """Validate if the column input is valid."""
    if len(col_input) != 1:
        return False
    
    col_char = col_input.upper()
    
    if not col_char.isalpha():
        return False
    
    col_index = ord(col_char) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_index(col_input):
    """Convert column letter to column index."""
    return ord(col_input.upper()) - ord('A')


def can_place_checker(board, col_index, rows):
    """Check if a checker can be placed in the given column."""
    return board[0][col_index] == ' '


def place_checker(board, col_index, checker, rows):
    """Place a checker in the given column and return the row where it was placed."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker, rows, cols):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal (\), diagonal (/)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == ' ':
                return False
    return True


def get_player_move(board, player_num, checker, cols, rows):
    """Get a valid move from the player."""
    while True:
        col_input = input(f"Player {checker}, please enter a column: ")
        
        if not is_valid_column(col_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(col_input)
        
        if not can_place_checker(board, col_index, rows):
            print("That column is full. Please choose another column.")
            continue
        
        return col_index


def play_game(rows, cols, num_players):
    """Main game loop."""
    board = initialize_board(rows, cols)
    checkers = PLAYER_CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    print_board(board, cols)
    print(f"Game started! Player {checkers[current_player]} goes first.\n")
    
    while True:
        checker = checkers[current_player]
        col_index = get_player_move(board, current_player, checker, cols, rows)
        row_index = place_checker(board, col_index, checker, rows)
        
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row_index, col_index, checker, rows, cols):
            print(f"Player {checker} won!")
            return
        
        # Check for draw
        if is_board_full(board, rows, cols):
            print("It's a draw!")
            return
        
        # Move to next player
        current_player = (current_player + 1) % num_players


def main():
    """Main entry point of the program."""
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
