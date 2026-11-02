import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board(rows, columns):
    """Create the game board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    """Print the game board."""
    os.system('clear')
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(columns)))
    for row in board:
        print('+' + '---+' * columns)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * columns)

def is_valid_input(column_input, columns):
    """Check if the player's input is a valid column."""
    return len(column_input) == 1 and column_input.isalpha() and 'A' <= column_input <= chr(65 + columns - 1)

def get_next_open_row(board, column_index):
    """Return the row index of the first open space in the given column."""
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index
    return None  # Column is full

def winning_move(board, checker):
    """Check if the last move was a winning move."""
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical locations
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the board is full and a draw occurred."""
    return all(all(cell != ' ' for cell in row) for row in board)

def connect_four():
    """Main game loop for Connect 4."""
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board, COLUMNS)
        current_player = CHECKERS[current_player_index]
        print(f"Player {current_player}, please enter a column: ", end="")
        
        column_input = input().strip().upper()
        if not is_valid_input(column_input, COLUMNS):
            print("Invalid input! Try again.")
            continue
        
        column_index = ord(column_input) - 65
        row_index = get_next_open_row(board, column_index)
        
        if row_index is None:
            print("Column is full! You lose your turn.")
        else:
            board[row_index][column_index] = current_player
            if winning_move(board, current_player):
                print_board(board, COLUMNS)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board, COLUMNS)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    connect_four()
