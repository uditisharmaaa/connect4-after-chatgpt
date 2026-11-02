import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+---' * COLS + '+')

def is_valid_column_letter(letter):
    """Check if the input letter is a valid column."""
    if len(letter) != 1:
        return False
    return 'A' <= letter.upper() <= chr(65 + COLS - 1)

def get_column_index(letter):
    """Convert column letter to zero-based index."""
    return ord(letter.upper()) - 65

def is_column_full(board, col):
    """Check if the column is full."""
    return board[0][col] != ' '

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, row, col, checker):
    """Check if placing the checker at (row, col) causes a win."""
    # Directions: (dr, dc) for down-right, down, down-left, right
    directions = [(1, 1), (1, 0), (1, -1), (0, 1)]
    
    for dr, dc in directions:
        count = 1  # current checker already counts as 1
        
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def main():
    board = initialize_board()
    players = PLAYERS
    current_player = random.randint(0, players - 1)
    
    while True:
        clear_screen()
        print_board(board)
        
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        
        while True:
            column_letter = input().strip().upper()
            if is_valid_column_letter(column_letter):
                col = get_column_index(column_letter)
                if not is_column_full(board, col):
                    break
                else:
                    print("Column is full. Try another column: ", end='')
            else:
                print("Invalid input. Please enter a valid column (A-" + chr(65 + COLS - 1) + "): ", end='')
        
        # Place the checker
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = checker
                
                # Check for win
                if check_win(board, row, col, checker):
                    clear_screen()
                    print_board(board)
                    print(f"Player {checker} won!")
                    return
                
                break
        
        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            return
        
        # Next player's turn
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
