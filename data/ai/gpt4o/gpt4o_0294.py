import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players
NUM_PLAYERS = 2  # Number of players for this submission

def create_board(rows, columns):
    """Create a game board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    column_labels = '  '.join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_char):
    """Check if the input character is a valid column."""
    return input_char.isalpha() and 'A' <= input_char < chr(65 + COLUMNS)

def get_available_row(board, column_index):
    """Find the lowest available row in a given column."""
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index
    return None  # Column is full

def place_checker(board, column_index, player_symbol):
    """Place the player's checker in the specified column."""
    row_index = get_available_row(board, column_index)
    if row_index is not None:
        board[row_index][column_index] = player_symbol
        return True
    return False  # Column is full

def check_for_win(board, player_symbol):
    """Check for a win condition for the player symbol."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    
    # Check diagonal (\) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
    
    # Check diagonal (/) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    """Main game loop."""
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        player_symbol = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {player_symbol}, please enter a column:")
        while True:
            try:
                player_input = input().strip().upper()
                if not is_valid_input(player_input):
                    raise ValueError("Invalid input. Please enter a valid column.")
                column_index = ord(player_input) - ord('A')
                if not place_checker(board, column_index, player_symbol):
                    raise ValueError("Column is full. Please choose another column.")
                break
            except ValueError as e:
                print(e)

        print_board(board)

        # Check for win
        if check_for_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if check_for_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
