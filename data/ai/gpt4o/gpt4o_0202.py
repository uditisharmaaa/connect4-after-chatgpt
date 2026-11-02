import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """ Initializes and returns a 2D list representing the board. """
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """ Prints the current state of the board. """
    os.system('clear')  # Clear the screen for Unix/Linux systems
    column_labels = ' '.join([chr(65 + i) for i in range(len(board[0]))])
    print(f"  {column_labels}")
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * len(row) + '+')

def select_random_player(num_players):
    """ Randomly selects and returns the first player index. """
    return random.randint(0, num_players - 1)

def is_valid_column(input_column, columns):
    """ Checks if the input column is valid. """
    return input_column in [chr(65 + i) for i in range(columns)]

def make_move(board, player, column):
    """ Places a player's checker in the specified column of the board. """
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = CHECKERS[player]
            return True  # Move successful
    return False  # Column is full

def check_win(board, player, rows, columns):
    """ Checks if the current player has won the game. """
    checker = CHECKERS[player]

    # Check horizontal win
    for row in board:
        for col in range(columns - 3):
            if row[col:col + 4] == [checker] * 4:
                return True 

    # Check vertical win
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True 

    # Check diagonal win (bottom left to top right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True 

    # Check diagonal win (top left to bottom right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True 

    return False

def check_draw(board):
    """ Checks if the game is a draw (the board is full). """
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = select_random_player(PLAYERS)
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        # Validate input
        while not is_valid_column(user_input, COLUMNS):
            user_input = input(f"Invalid input. Player {player_checker}, please enter a column: ").strip().upper()
        
        # Make move
        if make_move(board, current_player, user_input):
            print_board(board)

            # Check for win
            if check_win(board, current_player, ROWS, COLUMNS):
                print(f"Player {player_checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break

            # Alternate turns
            current_player = (current_player + 1) % PLAYERS
        else:
            print(f"Column {user_input} is full. Player {player_checker} loses the turn.")

if __name__ == "__main__":
    main()
