import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Create and return an empty board with the specified dimensions.
    All cells are initialized with whitespace.
    """
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """
    Print the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print top border
    print('+' + '---+' * COLS)
    
    # Print each row with borders
    for row in range(ROWS):
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
        print('+' + '---+' * COLS)

def is_valid_column(board, col):
    """
    Check if a column is valid and has space available.
    Returns True if the column exists and has at least one empty cell.
    """
    if col < 0 or col >= COLS:
        return False
    # Check if top row of the column is empty
    return board[0][col] == ' '

def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if successful, False otherwise.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    Checks for 4 in a row horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if all cells in the top row are occupied.
    """
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(board, player_checker):
    """
    Get and validate player input for column selection.
    Continues asking until a valid input is received.
    """
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Validate input is a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(move) - ord('A')
        
        # Validate column is within board range
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Validate column has space
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def play_game():
    """
    Main game loop that handles the Connect 4 game.
    """
    # Initialize the board
    board = create_board()
    
    # Get the list of players for this game
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_checker)
        
        # Place the checker
        place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
