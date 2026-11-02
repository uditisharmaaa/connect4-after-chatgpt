import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Modify this to the number of players (between 2 and 5)

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board():
    """Creates the game board filled with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board in the required format."""
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(col_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Checks if a column is valid for a move."""
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == " "

def get_next_open_row(board, column):
    """Returns the next open row for a given column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            return row
    return -1

def drop_checker(board, row, column, checker):
    """Drops a checker into the specified row and column."""
    board[row][column] = checker

def check_for_win(board, checker):
    """Checks if the specified checker has won the game (4 in a row)."""
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(board[0][c] != " " for c in range(COLS))

def get_column_input(player, board):
    """Prompts the player for a valid column."""
    while True:
        try:
            column = input(f"Player {player}, please enter a column: ").strip().upper()
            if len(column) != 1 or not column.isalpha():
                raise ValueError
            column_index = ord(column) - 65
            if is_valid_column(column_index, board):
                return column_index
            else:
                print("Invalid move. Column is full or out of bounds.")
        except ValueError:
            print("Invalid input. Please enter a single column letter.")

def main():
    """Main game loop."""
    # Initialization
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    clear_screen()
    print("Welcome to Connect 4!")
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_idx]
        print_board(board)
        column = get_column_input(current_player, board)
        row = get_next_open_row(board, column)
        drop_checker(board, row, column, current_player)
        
        clear_screen()
        # Check for a win
        if check_for_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch turn to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
