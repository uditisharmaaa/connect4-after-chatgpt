import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    os.system('clear')
    # Print column letters
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print board rows
    for row in board:
        print('+' + ('---+' * COLS))
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print('+' + ('---+' * COLS))

def get_valid_column(board):
    """Prompt the current player for a valid column."""
    while True:
        column = input(f"Player {current_checker}, please enter a column: ").upper()
        if len(column) != 1:
            print("Please enter a single character.")
            continue
        col_num = ord(column) - ord('A')
        if col_num < 0 or col_num >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col_num] != ' ':
            print("Column is full. Try another column.")
            continue
        return col_num

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row][col+1] == checker and
                board[row][col+2] == checker and
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and
                board[row+1][col] == checker and
                board[row+2][col] == checker and
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row-1][col+1] == checker and
                board[row-2][col+2] == checker and
                board[row-3][col+3] == checker):
                return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

# Main game
def main():
    global current_checker
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_checker = random.choice(players)
    
    while True:
        print_board(board)
        col = get_valid_column(board)
        place_checker(board, col, current_checker)
        
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_idx = players.index(current_checker)
        current_checker = players[(current_idx + 1) % PLAYERS]

if __name__ == "__main__":
    main()
