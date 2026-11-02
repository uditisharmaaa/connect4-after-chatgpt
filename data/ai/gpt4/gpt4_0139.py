import os
import random

# Constants for game setup
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2  # Default is 2 players
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', ..., 'G']

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates a game board initialized with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))
    # Print rows with separators
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def get_valid_column_input(board):
    """Gets a valid column input from the player."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        # Validate input
        if column not in COLUMN_LABELS[:len(board[0])]:
            print("Invalid column. Try again.")
        else:
            column_index = COLUMN_LABELS.index(column)
            if board[0][column_index] != " ":
                print("Column is full. Choose another column.")
            else:
                return column_index

def drop_checker(board, column, checker):
    """Drops the checker into the chosen column."""
    for row in range(len(board) - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == " ":
            board[row][column] = checker
            return row

def check_for_win(board, player, row, col):
    """Checks if the latest move resulted in a win."""
    def count_consecutive(dx, dy):
        """Counts consecutive checkers along a given direction."""
        count = 0
        x, y = col, row
        while 0 <= y < len(board) and 0 <= x < len(board[0]) and board[y][x] == player:
            count += 1
            x += dx
            y += dy
        return count

    # Check all four directions: horizontal, vertical, diagonals
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        if count_consecutive(dx, dy) + count_consecutive(-dx, -dy) - 1 >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def play_connect4():
    """Main function to play the Connect 4 game."""
    # Initialize game variables
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    # Game loop
    while True:
        current_player = CHECKERS[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        
        # Get the player's column choice
        column = get_valid_column_input(board)
        row = drop_checker(board, column, current_player)
        
        # Print the updated board
        print_board(board)

        # Check for win
        if check_for_win(board, current_player, row, column):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    play_connect4()
