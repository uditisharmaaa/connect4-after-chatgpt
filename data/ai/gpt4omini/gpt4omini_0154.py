import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Allowed player symbols

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create an empty board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+' + '---+' * COLUMNS)
    
    # Print each row of the board
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def get_random_first_player(num_players):
    """Randomly select the first player from the available players."""
    return random.randint(0, num_players - 1)

def is_valid_input(column):
    """Check if the input column is valid (A-G)."""
    return column.isalpha() and len(column) == 1 and 'A' <= column.upper() <= chr(64 + COLUMNS)

def get_column_index(column):
    """Convert column letter to index (0-based)."""
    return ord(column.upper()) - 65

def drop_checker(board, column_index, checker):
    """Drop the checker into the specified column."""
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False  # No space in the column

def check_winner(board, checker):
    """Check for a win condition (horizontally, vertically, diagonally)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False  # No winner yet

def is_draw(board):
    """Check if the board is full (draw condition)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to control the game flow."""
    board = create_board()  # Initialize the game board
    num_players = 2  # Set the number of players
    current_player = get_random_first_player(num_players)  # Randomly select first player
    game_over = False
    
    while not game_over:
        print_board(board)  # Display the board
        checker = PLAYER_SYMBOLS[current_player]  # Determine current player's checker
        
        # Player input loop
        while True:
            column = input(f"Player {checker}, please enter a column: ")
            if is_valid_input(column):
                column_index = get_column_index(column)
                if drop_checker(board, column_index, checker):
                    break  # Valid move, exit input loop
                else:
                    print("Column is full! Please try again.")
            else:
                print("Invalid input! Please enter a letter from A to G.")

        # Check for a win or draw
        if check_winner(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        
        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Start the game
if __name__ == "__main__":
    play_game()
