import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    """Initialize an empty game board with given dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Print column headers
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print each row with borders
    border = "+" + ("---+" * COLS)
    for row in board:
        print(border)
        print("| " + " | ".join(row) + " |")
    print(border)

def get_player_symbols(num_players):
    """Return list of player symbols based on number of players."""
    symbols = ["X", "O", "V", "H", "M"]
    return symbols[:num_players]

def get_random_first_player(num_players):
    """Return a random player index to start the game."""
    return random.randint(0, num_players - 1)

def is_valid_column_input(column):
    """Check if user input is a valid column letter."""
    return len(column) == 1 and column.isalpha() and column.upper() < chr(65 + COLS)

def drop_checker(board, col, symbol):
    """
    Attempt to drop a checker into the specified column.
    Returns True if successful, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    return False

def check_win(board, symbol):
    """Check if the specified symbol has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled."""
    return all(cell != " " for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    player_symbols = get_player_symbols(PLAYERS)
    current_player = get_random_first_player(PLAYERS)
    
    clear_screen()
    print(f"Player {player_symbols[current_player]} starts first!")
    print_board(board)
    
    while True:
        symbol = player_symbols[current_player]
        prompt = f"Player {symbol}, please enter a column: "
        while True:
            col_input = input(prompt).upper()
            if not is_valid_column_input(col_input):
                print(f"Invalid input! Please enter a letter between A and {chr(65 + COLS - 1)}")
                continue
            
            col = ord(col_input) - 65  # Convert to 0-based index
            if board[0][col] != " ":
                print("That column is full! Please choose another.")
                continue
            
            break
        
        clear_screen()
        drop_checker(board, col, symbol)
        print_board(board)
        
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break
        
        if is_board_full(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
