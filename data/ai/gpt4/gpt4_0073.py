import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_MARKS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def create_board(rows, cols):
    """Creates the game board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    # Print rows of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(column, cols):
    """Checks if the column input is valid."""
    return len(column) == 1 and column.isalpha() and 'A' <= column < chr(65 + cols)

def make_move(board, col, player_mark):
    """Places the player's marker on the board."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = player_mark
            return True
    return False

def check_winner(board, player_mark):
    """Checks if the player has won."""
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_mark for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player_mark for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right) check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_mark for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right) check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_mark for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell != EMPTY_CELL for row in board for cell in row)

def get_player_input(valid_cols):
    """Gets a column choice from the player."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        if is_valid_input(column, COLS):
            col_index = ord(column) - 65
            if col_index in valid_cols:
                return col_index
        print("Invalid input. Try again.")

def main():
    # Game setup
    board = create_board(ROWS, COLS)
    num_players = 2  # Fixed to 2 players for this assignment
    players = PLAYER_MARKS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        # Current player's turn
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        valid_columns = [col for col in range(COLS) if board[0][col] == EMPTY_CELL]
        if not valid_columns:
            print("The game is a draw!")
            break
        col = get_player_input(valid_columns)
        if make_move(board, col, current_player):
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
