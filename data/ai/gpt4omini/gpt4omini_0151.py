import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
WINNING_LENGTH = 4

def create_board():
    """Create a new game board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the console (Unix)
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_input(column):
    """Check if the input is valid (a letter A-G)."""
    return column in (chr(ord('A') + i) for i in range(COLS))

def get_column_index(column):
    """Convert column letter to index."""
    return ord(column) - ord('A')

def place_checker(board, column, player):
    """Place a checker on the board in the given column."""
    col_index = get_column_index(column)
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player
            return True
    return False  # The column is full

def check_win(board, player):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WINNING_LENGTH + 1):
            if all(board[row][col + i] == player for i in range(WINNING_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WINNING_LENGTH + 1):
            if all(board[row + i][col] == player for i in range(WINNING_LENGTH)):
                return True

    # Check diagonal (bottom left to top right)
    for row in range(ROWS - WINNING_LENGTH + 1):
        for col in range(COLS - WINNING_LENGTH + 1):
            if all(board[row + i][col + i] == player for i in range(WINNING_LENGTH)):
                return True

    # Check diagonal (top left to bottom right)
    for row in range(WINNING_LENGTH - 1, ROWS):
        for col in range(COLS - WINNING_LENGTH + 1):
            if all(board[row - i][col + i] == player for i in range(WINNING_LENGTH)):
                return True

    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        player = PLAYERS[current_player_index]
        print(f"Player {player}, please enter a column (A-G): ")
        
        column = input().upper()
        while not is_valid_input(column):
            print("Invalid input. Please enter a valid column (A-G): ")
            column = input().upper()

        if place_checker(board, column, player):
            print_board(board)

            if check_win(board, player):
                print(f"Player {player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            
            # Move to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full, please choose another column.")

if __name__ == "__main__":
    main()
