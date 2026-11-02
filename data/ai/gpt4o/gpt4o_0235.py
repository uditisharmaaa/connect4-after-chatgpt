import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates the game board with specified dimensions."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    column_labels = '  '.join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print("+---" * COLUMNS + "+")

def is_valid_column(input_column):
    """Checks if the input column is valid and returns the column index."""
    if len(input_column) != 1:
        return False
    column_index = ord(input_column.upper()) - 65
    return 0 <= column_index < COLUMNS

def get_lowest_empty_row(board, column_index):
    """Gets the index of the lowest empty row in the specified column."""
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index
    return None

def place_checker(board, column_index, checker):
    """Places the checker in the specified column."""
    row_index = get_lowest_empty_row(board, column_index)
    if row_index is not None:
        board[row_index][column_index] = checker
        return True
    return False

def check_for_win(board):
    """Checks for a win condition on the board."""
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != ' ':
                # Horizontal
                if col <= COLUMNS - 4 and all(board[row][col+i] == board[row][col] for i in range(4)):
                    return True
                # Vertical
                if row <= ROWS - 4 and all(board[row+i][col] == board[row][col] for i in range(4)):
                    return True
                # Diagonal /
                if row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row+i][col+i] == board[row][col] for i in range(4)):
                    return True
                # Diagonal \
                if row >= 3 and col <= COLUMNS - 4 and all(board[row-i][col+i] == board[row][col] for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    print_board(board)
    
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        while True:
            input_column = input().strip()
            if is_valid_column(input_column):
                column_index = ord(input_column.upper()) - 65
                if place_checker(board, column_index, current_checker):
                    break
                else:
                    print("Column is full. Choose another column:")
            else:
                print("Invalid input. Please enter a valid column:")
        
        print_board(board)
        
        if check_for_win(board):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
