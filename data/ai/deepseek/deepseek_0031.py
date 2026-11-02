import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a new board filled with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(len(board[0]))]))
    
    # Print top border
    print('+' + ('---+' * len(board[0])))
    
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + ('---+' * len(board[0])))

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if not col.isalpha() or len(col) != 1:
        return False
    col_index = ord(col.upper()) - ord('A')
    return 0 <= col_index < len(board[0]) and board[0][col_index] == ' '

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the column."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True
    
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (a draw)."""
    return all(cell != ' ' for cell in board[0])

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        clear_screen()
        print_board(board)
        
        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("Game ended in a draw.")
            break
        
        print(f"Player {current_player}, please enter a column: ", end='')
        col = input().strip().upper()
        
        if is_valid_column(col, board):
            if place_checker(board, col, current_player):
                # Switch to the next player
                current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("Invalid column. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
