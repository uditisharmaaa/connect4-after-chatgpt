import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Creates a game board initialized with whitespace."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_input(column):
    """Checks if the column input is valid."""
    return len(column) == 1 and column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

def find_empty_row(board, col):
    """Finds the lowest available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def place_checker(board, col, checker):
    """Places a checker in the specified column if the column is not full."""
    if 0 <= col < COLS:
        row = find_empty_row(board, col)
        if row is not None:
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the given checker has won the game."""
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select starting player
    turn_index = PLAYERS.index(current_player)

    print_board(board)

    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()

        # Validate the input
        if not is_valid_input(column):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        col_index = ord(column) - 65  # Convert letter to column index

        # Try to place the checker
        if place_checker(board, col_index, current_player):
            print_board(board)  # Print the updated board

            # Check for a win
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break

            # Check for a draw
            if check_draw(board):
                print("The game is a draw!")
                break

            # Move to the next player
            turn_index = (turn_index + 1) % len(PLAYERS)
            current_player = PLAYERS[turn_index]
        else:
            print("Column is full. Please choose another column.")

if __name__ == '__main__':
    main()
