import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board."""
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(column, board):
    """Check if the chosen column is valid and not full."""
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

def drop_checker(column, board, checker):
    """Drop a checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_win(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_player_input(current_player, board):
    """Get a valid column input from the player."""
    while True:
        column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + COLUMNS - 1):
            column = ord(column_input) - ord('A')
            if is_valid_column(column, board):
                return column
            else:
                print("Column is full. Try another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def main():
    """Main game loop."""
    # Initialization
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Random start
    clear_screen()
    print_board(board)

    while True:
        # Current player's turn
        current_player = players[current_player_index]
        column = get_player_input(current_player, board)
        drop_checker(column, board, current_player)
        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
