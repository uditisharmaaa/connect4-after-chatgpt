import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board(rows, cols):
    """Create an empty game board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board to the console."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def get_valid_move(board, player):
    """Prompt the player for a valid move and return the column index."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(ord('A') + len(board[0]) - 1)))
            continue
        
        col = ord(move) - ord('A')
        if col < 0 or col >= len(board[0]):
            print("Column out of range. Please enter a letter between A and {}.".format(chr(ord('A') + len(board[0]) - 1)))
            continue
        
        # Check if column is not full
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won the game."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - 3):
        for col in range(3, cols):
            if all(board[row+i][col-i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        player = PLAYERS[current_player]
        col = get_valid_move(board, player)
        place_checker(board, col, player)
        print_board(board)
        
        if check_win(board, player):
            print(f"Player {player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
