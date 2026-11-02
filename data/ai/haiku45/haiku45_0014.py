import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """
    Create a board with specified dimensions, initialized with empty spaces.
    """
    board = []
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(" ")
        board.append(new_row)
    return board


def print_board(board):
    """
    Print the board in a formatted way with column labels and grid lines.
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with grid lines
    for row in range(rows):
        # Print top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def is_valid_input(user_input, cols):
    """
    Check if the user input is valid (single uppercase letter within board range).
    """
    if len(user_input) != 1:
        return False
    
    if not user_input.isalpha():
        return False
    
    user_input = user_input.upper()
    col_index = ord(user_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_index(user_input):
    """
    Convert user input (letter) to column index (integer).
    """
    return ord(user_input.upper()) - ord('A')


def is_column_full(board, col_index):
    """
    Check if a column is completely filled with checkers.
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """
    Check if there are 4 checkers in a row horizontally.
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, checker):
    """
    Check if there are 4 checkers in a row vertically.
    """
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, checker):
    """
    Check if there are 4 checkers in a row diagonally (both directions).
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonals going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the current player has won.
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_next_player(current_player, num_players):
    """
    Get the index of the next player.
    """
    return (current_player + 1) % num_players


def play_game():
    """
    Main game loop.
    """
    # Create board
    board = create_board(ROWS, COLS)
    
    # Create list of checkers for this game
    game_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = game_checkers[current_player]
        
        # Get valid input from player
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            
            if not is_valid_input(user_input, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = get_column_index(user_input)
            
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place checker
        place_checker(board, col_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("Draw! The board is full.")
            break
        
        # Move to next player
        current_player = get_next_player(current_player, NUM_PLAYERS)


# Run the game
if __name__ == "__main__":
    play_game()
