import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)])  # Column labels A, B, C, etc.
    print(header)
    print('+---' * COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLS + '+')

def is_valid_column(input_col, board):
    """Checks if the input column is valid."""
    if input_col.isalpha() and len(input_col) == 1:
        col = ord(input_col.upper()) - 65
        if 0 <= col < COLS and board[0][col] == ' ':
            return True
    return False

def get_lowest_empty_row(board, col):
    """Finds the lowest empty row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, col, checker):
    """Places a checker in the lowest available cell of the given column."""
    row = get_lowest_empty_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

def is_winner(board, checker):
    """Checks if the player with the given checker has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonals (\ direction)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonals (/ direction)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    # Initialize the game
    board = create_board(ROWS, COLS)
    num_players = 2  # Change this for more players (up to MAX_PLAYERS)
    checkers = CHECKERS[:num_players]
    
    current_player = random.randint(0, num_players - 1)  # Randomly choose the first player
    
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        print(f"Player {checkers[current_player]}, it's your turn!")
        
        # Get a valid column from the player
        while True:
            col_input = input("Please enter a column letter: ").strip()
            if is_valid_column(col_input, board):
                col = ord(col_input.upper()) - 65
                break
            else:
                print("Invalid input, please try again.")
        
        # Place the checker
        place_checker(board, col, checkers[current_player])
        
        clear_screen()
        print_board(board)

        # Check for win or draw
        if is_winner(board, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
