import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4


def create_board():
    """Create and initialize the game board with empty spaces."""
    board = []
    for row in range(ROWS):
        board.append([' ' for col in range(COLS)])
    return board


def print_board(board):
    """Print the game board with column labels and borders."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()


def is_valid_input(column_letter):
    """Check if the input is a valid column letter."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    column_index = ord(column_letter.upper()) - ord('A')
    if column_index < 0 or column_index >= COLS:
        return False
    return True


def is_column_full(board, column_index):
    """Check if a column is completely filled."""
    return board[0][column_index] != ' '


def place_checker(board, column_index, checker):
    """Place a checker in the lowest available space in the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return True
    return False


def check_horizontal_win(board, checker):
    """Check if there is a horizontal win."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """Check if there is a vertical win."""
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """Check if there is a diagonal win (both directions)."""
    # Check diagonal going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
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
    """Check if the board is completely full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True


def play_game():
    """Main game loop."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ").upper()
            
            if not is_valid_input(column_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column_index = ord(column_input) - ord('A')
            
            if is_column_full(board, column_index):
                print("Column is full. Please choose another column.")
                continue
            
            # Valid input, place checker
            place_checker(board, column_index, current_checker)
            break
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
