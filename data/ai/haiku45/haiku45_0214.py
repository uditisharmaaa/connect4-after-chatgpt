import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a board with specified dimensions, initialized with empty spaces."""
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            board_row.append(" ")
        board.append(board_row)
    return board

def print_board(board):
    """Print the board with column labels and grid lines."""
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()

def get_valid_input(board, player_checker):
    """Get valid column input from player."""
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - 65
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, player_checker):
    """Place checker in the specified column and return True if successful."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    return False

def check_horizontal_win(board, player_checker):
    """Check if player has won horizontally."""
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_vertical_win(board, player_checker):
    """Check if player has won vertically."""
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_diagonal_right_win(board, player_checker):
    """Check if player has won diagonally (top-left to bottom-right)."""
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_diagonal_left_win(board, player_checker):
    """Check if player has won diagonally (top-right to bottom-left)."""
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, player_checker):
    """Check if the player has won."""
    return (check_horizontal_win(board, player_checker) or
            check_vertical_win(board, player_checker) or
            check_diagonal_right_win(board, player_checker) or
            check_diagonal_left_win(board, player_checker))

def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Create board
    board = create_board(ROWS, COLS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Choose random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_won = False
    
    while not game_won:
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid input and place checker
        col = get_valid_input(board, current_player_checker)
        place_checker(board, col, current_player_checker)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_won = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_won = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    play_game()

if __name__ == "__main__":
    main()
