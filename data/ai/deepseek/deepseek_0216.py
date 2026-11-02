import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    os.system('clear' if os.name == 'posix' else 'cls')
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print the board
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def get_valid_move(player):
    """Get a valid column input from the player."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or move not in [chr(65 + i) for i in range(COLS)]:
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
        else:
            return ord(move) - ord('A')

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has four checkers in a row (horizontally, vertically, or diagonally)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_move(current_player)
        if not place_checker(board, col, current_player):
            print(f"Column {chr(65 + col)} is full. Player {current_player} loses their turn.")
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
