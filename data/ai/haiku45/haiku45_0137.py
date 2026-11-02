import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def create_board(rows, columns):
    """Create a board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    columns = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for i in range(columns):
        letter = chr(ord('A') + i)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row_idx in range(rows):
        # Print top border
        print("+", end="")
        for col_idx in range(columns):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col_idx in range(columns):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col_idx in range(columns):
        print("---+", end="")
    print()

def get_valid_input(columns, board):
    """Get valid column input from player."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_idx = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_idx < 0 or col_idx >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_idx] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_idx

def place_checker(board, col_idx, checker):
    """Place a checker in the specified column and return the row index."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row_idx in range(rows - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx
    
    return -1

def check_horizontal_win(board, row_idx, col_idx, checker):
    """Check if there is a horizontal win."""
    columns = len(board[0])
    count = 0
    
    # Count checkers to the left
    for i in range(col_idx, -1, -1):
        if board[row_idx][i] == checker:
            count += 1
        else:
            break
    
    # Count checkers to the right (excluding the current one)
    for i in range(col_idx + 1, columns):
        if board[row_idx][i] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_vertical_win(board, row_idx, col_idx, checker):
    """Check if there is a vertical win."""
    rows = len(board)
    count = 0
    
    # Count checkers above
    for i in range(row_idx, -1, -1):
        if board[i][col_idx] == checker:
            count += 1
        else:
            break
    
    # Count checkers below (excluding the current one)
    for i in range(row_idx + 1, rows):
        if board[i][col_idx] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_diagonal_win(board, row_idx, col_idx, checker):
    """Check if there is a diagonal win (both directions)."""
    rows = len(board)
    columns = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    count = 0
    r, c = row_idx, col_idx
    
    # Count up and to the left
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c -= 1
    
    # Count down and to the right (excluding the current one)
    r, c = row_idx + 1, col_idx + 1
    while r < rows and c < columns:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 0
    r, c = row_idx, col_idx
    
    # Count up and to the right
    while r >= 0 and c < columns:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c += 1
    
    # Count down and to the left (excluding the current one)
    r, c = row_idx + 1, col_idx - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False

def check_win(board, row_idx, col_idx, checker):
    """Check if the current move results in a win."""
    if check_horizontal_win(board, row_idx, col_idx, checker):
        return True
    if check_vertical_win(board, row_idx, col_idx, checker):
        return True
    if check_diagonal_win(board, row_idx, col_idx, checker):
        return True
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Create board
    board = create_board(ROWS, COLUMNS)
    
    # Initialize players
    players = CHECKERS[:NUM_PLAYERS]
    
    # Select random starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_checker = players[current_player_idx]
        
        # Get valid input from player
        col_idx = get_valid_input(COLUMNS, board)
        
        # Place checker
        row_idx = place_checker(board, col_idx, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_idx, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print(f"Player {players[current_player_idx]}, please enter a column:")

# Run the game
if __name__ == "__main__":
    play_game()
