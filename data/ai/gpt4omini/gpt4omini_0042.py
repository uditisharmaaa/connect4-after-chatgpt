import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')  # Clear the console for updated board view
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column headers
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def create_board():
    """Creates a new game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def get_valid_column():
    """Prompts the player for a valid column input, returns the corresponding index."""
    while True:
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            return ord(column) - 65
        else:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, player):
    """Drops a checker for the current player in the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Checks if the current player has won the game."""
    # Check horizontal, vertical and diagonal (both directions) for a win
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == player for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == player for i in range(4)):
                    return True
                # Check diagonal (bottom-right)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player for i in range(4)):
                    return True
                # Check diagonal (bottom-left)
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the board is full and the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

# Game setup
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)
game_over = False

# Game loop
while not game_over:
    print_board(board)
    current_player = PLAYERS[current_player_index]
    
    # Get valid column input from the player
    col = get_valid_column()
    
    # Try to drop the checker in the selected column
    if drop_checker(board, col, current_player):
        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
    else:
        print("Column is full, please choose another column.")
