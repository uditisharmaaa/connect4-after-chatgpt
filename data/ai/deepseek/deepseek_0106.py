import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

def initialize_board():
    """
    Initialize an empty game board with ROWS x COLS dimensions.
    Each cell is initialized with a whitespace (" ").
    """
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """
    Print the game board with column headers and borders.
    """
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the board with borders
    border = "+" + ("---+" * COLS)
    print(border)
    for row in board:
        print("| " + " | ".join(cell if cell != " " else " " for cell in row) + " |")
        print(border)

def get_player_checkers(num_players):
    """
    Return a list of player checkers based on the number of players.
    Checkers are chosen in order: X, O, V, H, M for up to 5 players.
    """
    checkers = ["X", "O", "V", "H", "M"]
    return checkers[:num_players]

def is_valid_column(col_input, cols):
    """
    Check if the column input is valid (uppercase letter within range).
    """
    if len(col_input) != 1:
        return False
    col_char = col_input.upper()
    return col_char.isalpha() and ord(col_char) - ord('A') < cols

def get_column_index(col_char):
    """
    Convert a column character (e.g., 'A') to a column index (e.g., 0).
    """
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_idx, player_checker):
    """
    Place the player's checker in the lowest available row of the specified column.
    Returns True if placement was successful, False if column is full.
    """
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_checker
            return True
    return False

def check_win(board, player_checker):
    """
    Check if the player has won by getting 4 in a row (horizontally, vertically, or diagonally).
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontally
    for row in range(rows):
        for col in range(cols - 3):
            if (board[row][col] == player_checker and
                board[row][col+1] == player_checker and
                board[row][col+2] == player_checker and
                board[row][col+3] == player_checker):
                return True
    
    # Check vertically
    for row in range(rows - 3):
        for col in range(cols):
            if (board[row][col] == player_checker and
                board[row+1][col] == player_checker and
                board[row+2][col] == player_checker and
                board[row+3][col] == player_checker):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if (board[row][col] == player_checker and
                board[row+1][col+1] == player_checker and
                board[row+2][col+2] == player_checker and
                board[row+3][col+3] == player_checker):
                return True
    
    # Check diagonally (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if (board[row][col] == player_checker and
                board[row-1][col+1] == player_checker and
                board[row-2][col+2] == player_checker and
                board[row-3][col+3] == player_checker):
                return True
    
    return False

def is_board_full(board):
    """
    Check if the board is full (no empty spaces left).
    """
    for row in board:
        if " " in row:
            return False
    return True

def play_game():
    """
    Main function to play the Connect 4 game.
    """
    board = initialize_board()
    players = get_player_checkers(NUM_PLAYERS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_idx]
    
    print("Welcome to Connect 4!")
    print(f"Player {current_player} starts first!")
    
    while True:
        print_board(board)
        
        while True:
            col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if is_valid_column(col_input, COLS):
                col_idx = get_column_index(col_input)
                if place_checker(board, col_idx, current_player):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        current_player = players[current_player_idx]

# Start the game
if __name__ == "__main__":
    play_game()
