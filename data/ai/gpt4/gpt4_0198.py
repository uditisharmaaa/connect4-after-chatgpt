import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]
EMPTY_CELL = " "

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty game board."""
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_input(board, columns):
    """Prompts the player for a valid column input."""
    while True:
        column_choice = input("Please enter a column: ").strip().upper()
        if len(column_choice) == 1 and 'A' <= column_choice < chr(65 + columns):
            col_index = ord(column_choice) - 65
            if board[0][col_index] == EMPTY_CELL:
                return col_index
            else:
                print(f"Column {column_choice} is full. Try again.")
        else:
            print("Invalid input. Please enter a valid column.")

def place_checker(board, column, checker):
    """Places a checker in the specified column."""
    for row in reversed(board):
        if row[column] == EMPTY_CELL:
            row[column] = checker
            return

def check_winner(board, rows, cols):
    """Checks if a player has won the game."""
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] != EMPTY_CELL and \
               board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3]:
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] != EMPTY_CELL and \
               board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]:
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] != EMPTY_CELL and \
               board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3]:
                return True

    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] != EMPTY_CELL and \
               board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3]:
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != EMPTY_CELL for c in range(len(board[0])))

def connect_4():
    """Main function to play the Connect 4 game."""
    # Initialize game variables
    players = 2  # Change as needed
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, players - 1)

    print_board(board)

    # Main game loop
    while True:
        print(f"Player {CHECKERS[current_player_index]}'s turn.")
        column = get_valid_input(board, COLUMNS)
        place_checker(board, column, CHECKERS[current_player_index])
        print_board(board)

        # Check for a winner
        if check_winner(board, ROWS, COLUMNS):
            print(f"Player {CHECKERS[current_player_index]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % players

# Run the game
if __name__ == "__main__":
    connect_4()
