import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player_symbol):
    """Get and return valid column input from player."""
    prompt = f"Player {player_symbol}, please enter a column: "
    return input(prompt).strip().upper()

def is_valid_column(col_input):
    """Check if the column input is valid."""
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col_index = ord(col_input) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != " "

def place_checker(board, col_index, player_symbol):
    """Place a checker in the specified column. Returns True if successful, False if column is full."""
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_symbol
            return True
    return False

def check_horizontal_win(board, player_symbol):
    """Check for horizontal win."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical_win(board, player_symbol):
    """Check for vertical win."""
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_win(board, player_symbol):
    """Check for diagonal win (both directions)."""
    # Check diagonal down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, player_symbol):
    """Check if the current player has won."""
    return (check_horizontal_win(board, player_symbol) or
            check_vertical_win(board, player_symbol) or
            check_diagonal_win(board, player_symbol))

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_player = players[current_player_index]
        
        # Get valid input from player
        while True:
            col_input = get_column_input(current_player)
            
            if not is_valid_column(col_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(col_input) - 65
            
            if is_column_full(board, col_index):
                print("Column is full. You lose your turn.")
                break
            
            # Place the checker
            if place_checker(board, col_index, current_player):
                break
        
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
