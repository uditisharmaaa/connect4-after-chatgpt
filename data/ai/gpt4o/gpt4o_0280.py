import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
MAX_PLAYERS = 5

def create_board(rows, cols):
    """Create a board with the specified dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    print('+---' * COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLS + '+')

def get_next_open_row(board, col):
    """Find the next open row in the given column."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def is_valid_column(board, col):
    """Check if the column is a valid move."""
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(board, row, col, checker):
    """Place a checker on the board."""
    board[row][col] = checker

def check_for_win(board, checker):
    """Check if the current checker has won the game."""
    # Check horizontal locations for a win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == checker and all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical locations for a win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == checker and all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Check if the board is filled up and thus a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    
    current_player = random.randint(0, PLAYERS - 1)
    game_over = False

    while not game_over:
        checker = CHECKERS[current_player]
        valid_move = False
        
        while not valid_move:
            col = input(f"Player {checker}, please enter a column: ").upper()
            
            if col.isalpha() and 'A' <= col <= chr(ord('A') + COLS - 1):
                col_index = ord(col) - ord('A')
                if is_valid_column(board, col_index):
                    row = get_next_open_row(board, col_index)
                    if row is not None:
                        place_checker(board, row, col_index, checker)
                        valid_move = True
                        
        print_board(board)

        if check_for_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        elif check_for_draw(board):
            print("Game is a draw!")
            game_over = True

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
