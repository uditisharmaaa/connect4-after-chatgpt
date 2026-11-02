import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create an empty board with specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels
    col_labels = [chr(65 + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(col_labels))
    
    # Print the board rows
    border = '+' + ('---+' * BOARD_COLS)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def get_valid_move(board, player):
    """Prompt the player for a valid move until one is given."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(65 + BOARD_COLS - 1)))
            continue
        
        col = ord(move) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print(f"Column out of range. Please choose between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (down-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_valid_move(board, current_player)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
