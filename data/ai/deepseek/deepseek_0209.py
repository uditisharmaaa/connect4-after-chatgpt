import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print('+---+' * COLS)

def get_valid_column(board):
    """Prompt the user for a column and validate it."""
    while True:
        col_input = input("Player {}, please enter a column: ".format(current_player + 1)).upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter from A to {}.".format(chr(65 + COLS - 1)))
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print("Column out of range. Please enter a letter from A to {}.".format(chr(65 + COLS - 1)))
            continue
        
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the current move resulted in a win."""
    # Check horizontal
    for c in range(col - 3, col + 1):
        if c >= 0 and c + 3 < COLS:
            if all(board[row][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for r in range(row - 3, row + 1):
        if r >= 0 and r + 3 < ROWS:
            if all(board[r + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r, c in zip(range(row - 3, row + 1), range(col - 3, col + 1)):
        if r >= 0 and c >= 0 and r + 3 < ROWS and c + 3 < COLS:
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r, c in zip(range(row + 3, row - 1, -1), range(col - 3, col + 1)):
        if r - 3 >= 0 and c >= 0 and r < ROWS and c + 3 < COLS:
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    global current_player
    os.system('clear')
    
    # Initialize game
    board = initialize_board()
    checkers = ['X', 'O', 'V', 'H', 'M']
    current_player = random.randint(0, PLAYERS - 1)
    
    # Main game loop
    while True:
        print_board(board)
        print("Player {}'s turn ({})".format(current_player + 1, checkers[current_player]))
        
        col = get_valid_column(board)
        row = place_checker(board, col, checkers[current_player])
        
        if check_win(board, row, col, checkers[current_player]):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(current_player + 1))
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS
        os.system('clear')

if __name__ == "__main__":
    main()
