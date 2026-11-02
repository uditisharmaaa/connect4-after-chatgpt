import os
import random

# Constants for the game settings
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clears the terminal screen
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+---' + '---' * (COLS - 1) + '+')
    
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' + '---' * (COLS - 1) + '+')

def is_column_full(board, column):
    """Check if the specified column is full."""
    return board[0][column] != ' '

def drop_checker(board, column, checker):
    """Drop the checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontally
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertically
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G):")
        
        while True:
            try:
                column_input = input().strip().upper()  # Read input and clean it
                if len(column_input) != 1 or column_input < 'A' or column_input > chr(64 + COLS):
                    raise ValueError("Invalid input.")
                
                column = ord(column_input) - 65  # Convert column letter to index
                if is_column_full(board, column):
                    print("Column is full. Try another column.")
                else:
                    drop_checker(board, column, current_player)
                    break  # Break if the checker was successfully placed

            except ValueError:
                print("Invalid input. Please enter a valid column (A-G).")
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
