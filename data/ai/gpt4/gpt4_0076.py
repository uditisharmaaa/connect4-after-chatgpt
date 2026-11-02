import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Possible player checkers
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Displays the Connect 4 board."""
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS[:COLUMNS]))
    print("+---" * COLUMNS + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if the column is valid and not full."""
    if column not in COLUMN_LABELS[:COLUMNS]:
        return False
    column_index = COLUMN_LABELS.index(column)
    return board[0][column_index] == ' '  # Check top-most cell for availability

def drop_checker(column, board, player_checker):
    """Places a player’s checker in the selected column."""
    column_index = COLUMN_LABELS.index(column)

    # Drop to the lowest empty row in the selected column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = player_checker
            return True
    return False  # Should not reach here if valid column is checked beforehand

def check_winner(board, player_checker):
    """Checks if the specified player has won."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Check vertical win
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Check diagonal down-right (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonal up-right (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    # Game setup
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)  # Randomly choose starting player

    clear_screen()
    print_board(board)

    while True:
        print(f"Player {players[current_player]}'s turn.")
        column = input("Please enter a column: ").strip().upper()

        # Validate the input column
        while not is_valid_column(column, board):
            print("Invalid column. Please try again.")
            column = input("Please enter a column: ").strip().upper()

        # Place checker and update the board
        drop_checker(column, board, players[current_player])

        clear_screen()
        print_board(board)

        # Check for a win or draw
        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
