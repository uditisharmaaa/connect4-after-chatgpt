import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # More players can be added if needed

def initialize_board():
    """Initializes the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board with column labels and borders."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, etc.)
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the board rows with borders
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---+' * COLS)

def get_random_first_player(num_players):
    """Returns a random player index to start the game."""
    return random.randint(0, num_players - 1)

def is_valid_column(column):
    """Checks if the column input is valid (uppercase letter within bounds)."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return col_char.isalpha() and ord(col_char) - ord('A') < COLS

def get_column_index(column):
    """Converts a column letter (e.g., 'A') to a 0-based index."""
    return ord(column.upper()) - ord('A')

def place_checker(board, column, checker):
    """Attempts to place the checker in the specified column.
    Returns True if successful, False if the column is full."""
    col_index = get_column_index(column)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the specified checker has a winning line (4 in a row)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (all cells filled)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player(NUM_PLAYERS)
    players = PLAYERS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        player_checker = players[current_player]
        print(f"Player {player_checker}, please enter a column: ", end='')
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        col_index = get_column_index(column)
        if not (0 <= col_index < COLS):
            print(f"Column {column} is out of bounds.")
            continue
        
        if not place_checker(board, column, player_checker):
            print(f"Column {column} is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
