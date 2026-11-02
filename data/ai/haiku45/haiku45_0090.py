import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """
    Creates and initializes the game board with empty spaces.
    Returns a 2D list with ROWS rows and COLS columns, all filled with spaces.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Prints the Connect 4 board in a formatted way with column labels and grid lines.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with grid
    for row in range(ROWS):
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()

def is_valid_column(column_input, board):
    """
    Validates if the column input is valid.
    - Must be a single uppercase letter
    - Must be within the board range
    - Column must not be completely filled
    Returns True if valid, False otherwise.
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not column_input.isupper() or not column_input.isalpha():
        return False
    
    # Convert letter to column index
    col_index = ord(column_input) - ord('A')
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not already full
    if board[0][col_index] != " ":
        return False
    
    return True

def get_player_move(board, player_checker):
    """
    Gets a valid move from the player.
    Keeps asking until a valid column is provided.
    Returns the column index (0-based).
    """
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if is_valid_column(column_input, board):
            return ord(column_input) - ord('A')
        else:
            print("Invalid input! Please enter a valid column letter.")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the specified column.
    The checker falls to the lowest available position.
    Returns the row index where the checker was placed.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return row
    
    # This should never happen if validation is correct
    return -1

def check_win(board, row, col, player_checker):
    """
    Checks if the current move results in a win for the player.
    Checks horizontally, vertically, and both diagonally.
    Returns True if there are 4 checkers in a row, False otherwise.
    """
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == player_checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == player_checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == player_checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == player_checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == player_checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == player_checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == player_checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == player_checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """
    Checks if the board is completely filled (draw condition).
    Returns True if the board is full, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """
    Main game loop. Initializes the game, alternates between players,
    and checks for win or draw conditions.
    """
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        current_player_checker = players[current_player_index]
        
        # Get player's move
        col_index = get_player_move(board, current_player_checker)
        
        # Place checker on the board
        row_index = place_checker(board, col_index, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
