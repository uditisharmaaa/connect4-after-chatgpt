import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+---' * COLS + '+')

def get_player_move(player):
    """Get the column from the player and validate it."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        return col

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the player has won with 4 in a row."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (a draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        col = get_player_move(checker)
        
        if not place_checker(board, col, checker):
            print("Column is full. You lose your turn.")
        
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
