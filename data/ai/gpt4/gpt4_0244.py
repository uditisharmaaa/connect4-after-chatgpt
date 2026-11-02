import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board(rows, cols):
    """Creates a 2D game board with empty spaces."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    horizontal_border = "+---" * len(board[0]) + "+"
    print(col_labels)
    for row in board:
        print(horizontal_border)
        print("| " + " | ".join(row) + " |")
    print(horizontal_border)

def get_valid_column(board):
    """Prompts the player until a valid column input is received."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        if len(column) == 1 and column.isalpha():
            col_index = ord(column) - 65
            if 0 <= col_index < len(board[0]) and board[0][col_index] == EMPTY_CELL:
                return col_index
        print("Invalid input. Try again.")

def drop_checker(board, col, token):
    """Drops the player's checker in the chosen column."""
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = token
            return

def check_winner(board, token):
    """Checks if the given player has won the game."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == token for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == token for i in range(4)):
                return True

    # Check diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True

    # Check diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == token for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != EMPTY_CELL for c in range(len(board[0])))

def play_game():
    """Main game function."""
    # Initialize game state
    clear_screen()
    board = initialize_board(ROWS, COLS)
    players = PLAYER_TOKENS[:2]  # Default to 2 players
    current_player = random.choice(players)

    # Game loop
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        # Get valid column and drop checker
        col = get_valid_column(board)
        drop_checker(board, col, current_player)
        
        # Check for win
        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
            
        # Switch players
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    play_game()
