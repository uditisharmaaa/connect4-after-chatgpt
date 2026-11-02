import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the game screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates a 2D board initialized with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    columns_labels = "   ".join([chr(65 + col) for col in range(len(board[0]))])  # A, B, C, ...
    print(f"  {columns_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_move(board, column):
    """Checks if the move is valid."""
    return 0 <= column < len(board[0]) and board[0][column] == " "

def drop_checker(board, column, checker):
    """Drops a checker into the chosen column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    """Checks for a win horizontally, vertically, and diagonally."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check positive diagonal
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check negative diagonal
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_column_input(board, player):
    """Gets a valid column input from the player."""
    while True:
        column_input = input(f"Player {player}, please enter a column: ").upper()
        if not column_input.isalpha() or len(column_input) != 1 or not ('A' <= column_input <= 'Z'):
            print("Invalid input. Please enter a valid column letter.")
            continue
        column = ord(column_input) - 65
        if is_valid_move(board, column):
            return column
        else:
            print("Column is either full or invalid. Try again.")

def main():
    """Main function to run the Connect 4 game."""
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Adjust this for more players, up to 5
    players = PLAYER_SYMBOLS[:num_players]
    random.shuffle(players)  # Shuffle player order
    current_player_index = 0  # Start with the first player
    game_over = False

    # Game loop
    while not game_over:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]
        
        # Get valid column input
        column = get_column_input(board, current_player)
        
        # Place checker
        drop_checker(board, column, current_player)
        
        # Check for win
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
            continue
        
        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            game_over = True
            continue
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
