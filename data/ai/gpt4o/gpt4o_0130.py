import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    column_labels = '  '.join([chr(65 + i) for i in range(COLUMNS)])
    print('  ' + column_labels)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_valid_column(board, player):
    """Get a valid column from the player."""
    while True:
        user_input = input(f"Player {player}, please enter a column: ").upper()
        if len(user_input) == 1 and 'A' <= user_input < chr(65 + COLUMNS):
            column = ord(user_input) - 65
            if board[0][column] == ' ':
                return column
            else:
                print("This column is full. Choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, checker):
    """Place the checker in the board."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_winner(board, checker):
    """Check if the given checker has won the game."""
    # Horizontal
    for row in board:
        for start in range(COLUMNS - 3):
            if row[start:start + 4] == [checker] * 4:
                return True
    
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    print_board(board)
    
    current_player = random.choice(range(PLAYERS))
    
    while True:
        column = get_valid_column(board, CHECKERS[current_player])
        place_checker(board, column, CHECKERS[current_player])
        
        print_board(board)
        
        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
