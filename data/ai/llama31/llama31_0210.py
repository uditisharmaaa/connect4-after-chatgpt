import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(columns, rows):
    """
    Create a 2D list representing the Connect 4 board
    """
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    """
    Print the current state of the board
    """
    print('  ' + ' '.join(string.ascii_uppercase[:columns]))
    for row in board:
        print('+---' * columns + '+')
        print('|   ' * columns + '|')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * columns + '+')

def get_player_checker(player_number):
    """
    Get the checker for a given player
    """
    return CHECKERS[player_number - 1]

def get_next_player(current_player):
    """
    Get the next player in the rotation
    """
    return (current_player % PLAYERS) + 1

def is_valid_input(input_string, columns):
    """
    Check if the user input is a valid column letter
    """
    return input_string.upper() in string.ascii_uppercase[:columns]

def get_column_index(column_letter):
    """
    Get the column index for a given column letter
    """
    return string.ascii_uppercase.index(column_letter.upper())

def is_column_full(board, column_index):
    """
    Check if a column is full
    """
    return board[0][column_index]!= ' '

def get_drop_position(board, column_index):
    """
    Get the row index where a checker should be placed
    """
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index
    return None

def check_for_win(board, row_index, column_index, checker):
    """
    Check if the current player has won
    """
    # Check horizontal
    count = 0
    for col in range(max(0, column_index - 3), min(BOARD_COLUMNS, column_index + 4)):
        if board[row_index][col] == checker:
            count += 1
        else:
            count = 0
        if count == 4:
            return True

    # Check vertical
    count = 0
    for row in range(max(0, row_index - 3), min(BOARD_ROWS, row_index + 4)):
        if board[row][column_index] == checker:
            count += 1
        else:
            count = 0
        if count == 4:
            return True

    # Check diagonal (top-left to bottom-right)
    count = 0
    for row, col in zip(range(max(0, row_index - 3), min(BOARD_ROWS, row_index + 4)),
                        range(max(0, column_index - 3), min(BOARD_COLUMNS, column_index + 4))):
        if board[row][col] == checker:
            count += 1
        else:
            count = 0
        if count == 4:
            return True

    # Check diagonal (bottom-left to top-right)
    count = 0
    for row, col in zip(range(max(0, row_index - 3), min(BOARD_ROWS, row_index + 4)),
                        range(max(0, column_index - 3), min(BOARD_COLUMNS, column_index + 4))):
        if board[row][BOARD_COLUMNS - 1 - col] == checker:
            count += 1
        else:
            count = 0
        if count == 4:
            return True

    return False

def is_board_full(board):
    """
    Check if the board is full
    """
    return all(board[0][col]!= ' ' for col in range(BOARD_COLUMNS))

def main():
    # Create the board
    board = create_board(BOARD_COLUMNS, BOARD_ROWS)

    # Randomly select the first player
    current_player = random.randint(1, PLAYERS)

    while True:
        os.system('clear')
        print_board(board, BOARD_COLUMNS)

        # Get the current player's checker
        checker = get_player_checker(current_player)

        # Ask the current player for their move
        while True:
            move = input(f"Player {checker}, please enter a column: ")
            if is_valid_input(move, BOARD_COLUMNS):
                column_index = get_column_index(move)
                if not is_column_full(board, column_index):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a letter.")

        # Drop the checker into the column
        drop_position = get_drop_position(board, column_index)
        board[drop_position][column_index] = checker

        # Check for a win
        if check_for_win(board, drop_position, column_index, checker):
            os.system('clear')
            print_board(board, BOARD_COLUMNS)
            print(f"Player {checker} won!")
            break

        # Check for a draw
        if is_board_full(board):
            os.system('clear')
            print_board(board, BOARD_COLUMNS)
            print("It's a draw!")
            break

        # Move to the next player
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
