import random
import os

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def create_board(rows, cols):
    """Create a new game board with all cells initialized to spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """Print the game board to the console."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
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
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print bottom border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()


def get_valid_input(player_checker, cols):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if the letter is within valid range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """Place a checker in the specified column. Returns True if successful."""
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_winner(board, last_row, last_col, player_checker):
    """Check if the last move resulted in a win."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    col = last_col - 1
    while col >= 0 and board[last_row][col] == player_checker:
        count += 1
        col -= 1
    # Check right
    col = last_col + 1
    while col < cols and board[last_row][col] == player_checker:
        count += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    row = last_row - 1
    while row >= 0 and board[row][last_col] == player_checker:
        count += 1
        row -= 1
    # Check down
    row = last_row + 1
    while row < rows and board[row][last_col] == player_checker:
        count += 1
        row += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    row = last_row - 1
    col = last_col - 1
    while row >= 0 and col >= 0 and board[row][col] == player_checker:
        count += 1
        row -= 1
        col -= 1
    # Check down-right
    row = last_row + 1
    col = last_col + 1
    while row < rows and col < cols and board[row][col] == player_checker:
        count += 1
        row += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    row = last_row - 1
    col = last_col + 1
    while row >= 0 and col < cols and board[row][col] == player_checker:
        count += 1
        row -= 1
        col += 1
    # Check down-left
    row = last_row + 1
    col = last_col - 1
    while row < rows and col >= 0 and board[row][col] == player_checker:
        count += 1
        row += 1
        col -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Create the board
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        player_checker = CHECKERS[current_player_index]
        
        # Get valid column input
        col = get_valid_input(player_checker, BOARD_COLUMNS)
        
        # Try to place the checker
        if place_checker(board, col, player_checker):
            # Find the row where the checker was placed
            for row in range(BOARD_ROWS):
                if board[row][col] == player_checker:
                    last_row = row
                    break
            
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_winner(board, last_row, col, player_checker):
                print(f"Player {player_checker} won!")
                game_over = True
            # Check for draw
            elif is_board_full(board):
                print("It's a draw!")
                game_over = True
            else:
                # Move to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Invalid move (column full), ask for input again
            print_board(board)


# Run the game
if __name__ == "__main__":
    play_game()
