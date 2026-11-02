import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    # Print column labels
    column_labels = [chr(65 + i) for i in range(COLS)]
    print('  ' + '   '.join(column_labels))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+---' * COLS + '+')

def is_valid_move(col, board):
    """Check if the move is valid (column exists and is not full)."""
    if not (0 <= col < COLS):
        return False
    return board[0][col] == ' '

def make_move(col, board, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the current player has won."""
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
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def get_column_input(player):
    """Get valid column input from the player."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            col = ord(col_input) - ord('A')
            if 0 <= col < COLS:
                return col
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}")
        except (ValueError, TypeError):
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}")

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_column_input(current_player)
        
        if not is_valid_move(col, board):
            print("Column is full. Please choose another column.")
            continue
        
        make_move(col, board, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
