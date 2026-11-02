import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return a 2D board with all cells initialized to spaces."""
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLUMNS):
            board_row.append(" ")
        board.append(board_row)
    return board


def print_board(board):
    """Print the board in the specified format with column labels and borders."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * COLUMNS + "+")
    
    # Print each row with borders
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * COLUMNS + "+")


def is_valid_column(col_letter):
    """Check if the column letter is valid."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_index = ord(col_letter.upper()) - ord('A')
    return 0 <= col_index < COLUMNS


def get_column_index(col_letter):
    """Convert a column letter to its index."""
    return ord(col_letter.upper()) - ord('A')


def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != " "


def get_next_available_row(board, col_index):
    """Find the next available row in a column (from bottom to top)."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1


def place_checker(board, col_index, checker):
    """Place a checker in the specified column."""
    row = get_next_available_row(board, col_index)
    if row != -1:
        board[row][col_index] = checker
        return True
    return False


def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def get_player_move(board, current_player, checker):
    """Get a valid move from the current player."""
    while True:
        user_input = input("Player " + checker + ", please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(user_input):
            print("Invalid input. Please enter a valid column letter (A-" + chr(ord('A') + COLUMNS - 1) + ").")
            continue
        
        col_index = get_column_index(user_input)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Choose random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get player move
        col_index = get_player_move(board, current_player, checker)
        
        # Place checker
        place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS


# Main program
if __name__ == "__main__":
    play_game()
