import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    The board has ROWS rows and COLS columns.
    """
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    Columns are labeled A, B, C, etc.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for col in range(COLS):
            print(board[row][col] + " | ", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_column(column_letter, board):
    """
    Checks if the column letter is valid and if the column has space.
    Returns True if valid, False otherwise.
    """
    # Check if input is a single character
    if len(column_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not column_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(column_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top row must be empty)
    if board[0][col_index] != " ":
        return False
    
    return True


def place_checker(board, column_letter, checker):
    """
    Places a checker in the specified column.
    The checker falls to the lowest available position.
    Returns True if successful, False otherwise.
    """
    col_index = ord(column_letter) - 65
    
    # Find the lowest empty row in this column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Checks if the specified checker has won the game.
    Checks horizontally, vertically, and diagonally.
    Returns True if the player has won, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False


def is_board_full(board):
    """
    Checks if the board is completely filled.
    Returns True if full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize board
    board = create_board()
    
    # Create list of players
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get player input
        valid_move = False
        while not valid_move:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            
            if is_valid_column(column_input, board):
                valid_move = True
                place_checker(board, column_input, current_checker)
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Start the game
if __name__ == "__main__":
    play_game()
