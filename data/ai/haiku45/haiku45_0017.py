import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, columns):
    """Create an empty board with the specified dimensions."""
    board = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    rows = len(board)
    columns = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        letter = chr(ord('A') + col)
        print(f"{letter}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---", end="")
        for col in range(columns - 1):
            print("+---", end="")
        print("+")
        
        # Print row content
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---", end="")
    for col in range(columns - 1):
        print("+---", end="")
    print("+")


def get_valid_column_input(board):
    """Get valid column input from the player."""
    columns = len(board[0])
    
    while True:
        user_input = input().strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-" + chr(ord('A') + columns - 1) + "):")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter:")
            continue
        
        # Convert letter to column index
        column_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if column_index < 0 or column_index >= columns:
            print("Invalid input. Please enter a letter (A-" + chr(ord('A') + columns - 1) + "):")
            continue
        
        # Check if column is full
        if board[0][column_index] != " ":
            print("Column is full. Please choose another column:")
            continue
        
        return column_index


def place_checker(board, column, player_checker):
    """Place the checker in the specified column and return the row where it was placed."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_checker
            return row
    
    return -1  # Column is full


def check_win(board, row, column, player_checker):
    """Check if the player has won after placing a checker at (row, column)."""
    rows = len(board)
    columns = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    col = column - 1
    while col >= 0 and board[row][col] == player_checker:
        count += 1
        col -= 1
    # Check right
    col = column + 1
    while col < columns and board[row][col] == player_checker:
        count += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][column] == player_checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][column] == player_checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, column - 1
    while r >= 0 and c >= 0 and board[r][c] == player_checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, column + 1
    while r < rows and c < columns and board[r][c] == player_checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, column + 1
    while r >= 0 and c < columns and board[r][c] == player_checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, column - 1
    while r < rows and c >= 0 and board[r][c] == player_checker:
        count += 1
        r += 1
        c -= 1
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
    
    # Create list of players
    players = []
    for i in range(NUM_PLAYERS):
        players.append(PLAYER_CHECKERS[i])
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        print(f"Player {current_player}, please enter a column:")
        column = get_valid_column_input(board)
        
        # Place the checker
        row = place_checker(board, column, current_player)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
