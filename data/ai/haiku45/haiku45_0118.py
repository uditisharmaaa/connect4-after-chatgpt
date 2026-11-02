import os
import random

# Game constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return an empty board with given dimensions."""
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            board_row.append(" ")
        board.append(board_row)
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def get_valid_column(board, num_players, current_player):
    """Get a valid column input from the current player."""
    cols = len(board[0])
    checker = PLAYER_CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if input is within the board range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """Place a checker in the specified column and return the row where it was placed."""
    checker = PLAYER_CHECKERS[current_player]
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_horizontal_win(board, rows, cols, row, col, player):
    """Check if there is a horizontal win at the given position."""
    checker = PLAYER_CHECKERS[player]
    count = 0
    
    # Check to the left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check to the right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    
    # Add 1 for the checker at col
    count += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, rows, cols, row, col, player):
    """Check if there is a vertical win at the given position."""
    checker = PLAYER_CHECKERS[player]
    count = 0
    
    # Check upward
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    # Check downward
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    
    # Add 1 for the checker at row
    count += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, rows, cols, row, col, player):
    """Check if there is a diagonal win (both directions) at the given position."""
    checker = PLAYER_CHECKERS[player]
    
    # Check diagonal from top-left to bottom-right
    count = 0
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    count += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 0
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    count += 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def check_win(board, row, col, player):
    """Check if the current player has won."""
    rows = len(board)
    cols = len(board[0])
    
    if check_horizontal_win(board, rows, cols, row, col, player):
        return True
    
    if check_vertical_win(board, rows, cols, row, col, player):
        return True
    
    if check_diagonal_win(board, rows, cols, row, col, player):
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
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get valid column input
        col = get_valid_column(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            checker = PLAYER_CHECKERS[current_player]
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("Draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


# Main entry point
if __name__ == "__main__":
    play_game()
