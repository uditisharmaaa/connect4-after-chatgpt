import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def get_player_move(player):
    """Get a valid column choice from the player."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(65 + COLS - 1)))
            continue
        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        # Check for draw before getting input
        if is_draw(board):
            print("The game is a draw!")
            break
        
        col = get_player_move(current_player)
        
        if not place_checker(board, col, current_player):
            print("Column is full! You lose your turn.")
            # Switch player after invalid move
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
            continue
        
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Switch player after valid move
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
