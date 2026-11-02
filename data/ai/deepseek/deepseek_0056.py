import random
import os

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board to the terminal."""
    # Print column headers
    headers = [chr(65 + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print board rows
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def is_valid_column(col_input):
    """Check if the column input is valid."""
    if len(col_input) != 1:
        return False
    col = col_input.upper()
    return col in [chr(65 + i) for i in range(BOARD_COLS)]

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible.
    Returns True if successful, False otherwise.
    """
    col_index = ord(col.upper()) - 65
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (down-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if (board[row][col] == checker and 
                board[row+1][col-1] == checker and 
                board[row+2][col-2] == checker and 
                board[row+3][col-3] == checker):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no more moves available)."""
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        os.system('clear')
        print_board(board)
        
        # Check for draw
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Get column input
        while True:
            col_input = input(f"Player {current_player}, please enter a column: ").strip()
            if is_valid_column(col_input):
                col = col_input.upper()
                if place_checker(board, col, current_player):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid column. Please enter a valid column (A-{}).".format(chr(65 + BOARD_COLS - 1)))
        
        # Check for win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Switch player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
