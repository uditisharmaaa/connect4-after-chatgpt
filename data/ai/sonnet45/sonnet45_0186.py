import random
import os

# Global constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates and returns an empty game board.
    Board is a 2D list with ROWS rows and COLS columns, initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    """
    Prints the current state of the board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print top border
    print("+" + "---+" * COLS)
    
    # Print each row with borders
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+" + "---+" * COLS)

def get_column_input(player_symbol):
    """
    Prompts the player for a column input and returns it.
    """
    user_input = input(f"Player {player_symbol}, please enter a column: ")
    return user_input

def is_valid_column(column_input):
    """
    Checks if the column input is a valid letter within the board range.
    Returns True if valid, False otherwise.
    """
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if not column_input.isupper():
        return False
    
    col_index = ord(column_input) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    
    return True

def is_column_full(board, col_index):
    """
    Checks if a column is completely full.
    Returns True if full, False otherwise.
    """
    return board[0][col_index] != " "

def place_checker(board, col_index, player_symbol):
    """
    Places a checker in the specified column for the given player.
    Returns True if successful, False if column is full.
    """
    # Check if column is full
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            return True
    
    return False

def check_win_horizontal(board, player_symbol):
    """
    Checks for a horizontal win (4 in a row).
    """
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    return False

def check_win_vertical(board, player_symbol):
    """
    Checks for a vertical win (4 in a column).
    """
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    return False

def check_win_diagonal_down(board, player_symbol):
    """
    Checks for a diagonal win (top-left to bottom-right direction).
    """
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    return False

def check_win_diagonal_up(board, player_symbol):
    """
    Checks for a diagonal win (bottom-left to top-right direction).
    """
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == player_symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    return False

def check_win(board, player_symbol):
    """
    Checks if the given player has won the game.
    Returns True if player has won, False otherwise.
    """
    if check_win_horizontal(board, player_symbol):
        return True
    if check_win_vertical(board, player_symbol):
        return True
    if check_win_diagonal_down(board, player_symbol):
        return True
    if check_win_diagonal_up(board, player_symbol):
        return True
    return False

def is_board_full(board):
    """
    Checks if the board is completely full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = create_board()
    
    # Create list of player symbols based on NUM_PLAYERS
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get valid input from player
        valid_move = False
        while not valid_move:
            column_input = get_column_input(current_player)
            
            # Validate input
            if not is_valid_column(column_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(column_input) - 65
            
            # Try to place checker
            if place_checker(board, col_index, current_player):
                valid_move = True
            else:
                print("Column is full. You lose your turn.")
                valid_move = True  # Move is "valid" but player loses turn
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
