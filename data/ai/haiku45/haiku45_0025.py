import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """Create and return an empty board with all whitespaces."""
    board = []
    for row in range(ROWS):
        new_row = []
        for col in range(COLUMNS):
            new_row.append(" ")
        board.append(new_row)
    return board

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        letter = chr(ord('A') + col)
        print(f" {letter} ", end="")
    print()
    
    # Print board with rows
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * COLUMNS + "+")

def get_next_available_row(board, col):
    """Return the next available row in a column, or -1 if full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def is_valid_input(user_input, board):
    """Check if the user input is valid."""
    if len(user_input) != 1:
        return False
    
    if not user_input.isalpha():
        return False
    
    col = ord(user_input.upper()) - ord('A')
    
    if col < 0 or col >= COLUMNS:
        return False
    
    if get_next_available_row(board, col) == -1:
        return False
    
    return True

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    row = get_next_available_row(board, col)
    if row != -1:
        board[row][col] = checker

def check_horizontal_win(board, checker):
    """Check if there is a horizontal win."""
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    return False

def check_vertical_win(board, checker):
    """Check if there is a vertical win."""
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    return False

def check_diagonal_win(board, checker):
    """Check if there is a diagonal win (both directions)."""
    # Check diagonal going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if (board[row][col] == checker and
                board[row + 1][col - 1] == checker and
                board[row + 2][col - 2] == checker and
                board[row + 3][col - 3] == checker):
                return True
    
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    if check_horizontal_win(board, checker):
        return True
    if check_vertical_win(board, checker):
        return True
    if check_diagonal_win(board, checker):
        return True
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        player_num = current_player + 1
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ")
            
            if is_valid_input(user_input, board):
                valid_input = True
            else:
                print("Invalid input. Please enter a valid column (A-" + chr(ord('A') + COLUMNS - 1) + ").")
        
        # Place checker on board
        col = ord(user_input.upper()) - ord('A')
        place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """Start the game."""
    play_game()

if __name__ == "__main__":
    main()
