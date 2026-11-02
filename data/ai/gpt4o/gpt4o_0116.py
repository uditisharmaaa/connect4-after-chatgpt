import random
import os

# Constants for the board dimensions and number of players
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + NUM_COLUMNS)]

def create_board():
    """Creates the game board."""
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+---' * NUM_COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * NUM_COLUMNS + '+')

def is_valid_input(input_char):
    """Validates user input for column."""
    return input_char in COLUMN_LABELS

def drop_checker(board, column, checker):
    """Drops the checker into the specified column if possible."""
    column_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_winner(board):
    """Checks if there is a winner on the board."""
    # Check horizontal, vertical, and diagonal for a connect 4
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            if board[row][col] != ' ' and (
                check_direction(board, row, col, 0, 1) or
                check_direction(board, row, col, 1, 0) or
                check_direction(board, row, col, 1, 1) or
                check_direction(board, row, col, 1, -1)
            ):
                return board[row][col]
    return None

def check_direction(board, row, col, delta_row, delta_col):
    """Checks if there are four same elements in a given direction."""
    checker = board[row][col]
    count = 0
    for i in range(4):
        r, c = row + i * delta_row, col + i * delta_col
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLUMNS and board[r][c] == checker:
            count += 1
    return count == 4

def check_draw(board):
    """Checks if the board is full and there is a draw."""
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

def main():
    """Main function to run the game."""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Randomly select the first player
    first_check = True

    while True:
        print_board(board)
        
        if first_check:
            print(f"Player {CHECKERS[current_player_index]}, please enter a column:")
            first_check = False
        
        column = input(f"Player {CHECKERS[current_player_index]}, please enter a column: ").strip().upper()
        while not is_valid_input(column) or not drop_checker(board, column, CHECKERS[current_player_index]):
            print("Invalid input. Try again.")
            column = input(f"Player {CHECKERS[current_player_index]}, please enter a column: ").strip().upper()

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
