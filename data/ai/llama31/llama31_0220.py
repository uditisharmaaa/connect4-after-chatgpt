import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """Create a 2D board with whitespaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    column_labels = string.ascii_uppercase[:len(board[0])]
    print('  ' + '   '.join(column_labels))
    print('+' + '+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '+---' * len(board[0]) + '+')

def get_random_player(players):
    """Return a random player index."""
    return random.randint(0, players - 1)

def get_player_checker(player_index):
    """Return the checker of the player."""
    return CHECKERS[player_index]

def get_valid_input(player_checker, board):
    """Get a valid column input from the player."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        if column_input in string.ascii_uppercase[:len(board[0])]:
            column_index = string.ascii_uppercase.index(column_input)
            if board[0][column_index]!= ' ':
                print("Column is already full. Please try again.")
            else:
                return column_index
        else:
            print("Invalid input. Please enter a column label.")

def place_checker(board, column_index, player_checker):
    """Place the checker in the lowest available space in the column."""
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            board[row_index][column_index] = player_checker
            return

def check_win(board, player_checker):
    """Check for a win in all directions."""
    # Horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == player_checker:
                return True

    # Vertical
    for column in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][column] == board[i+1][column] == board[i+2][column] == board[i+3][column] == player_checker:
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for column in range(len(board[0]) - 3):
            if board[row][column] == board[row+1][column+1] == board[row+2][column+2] == board[row+3][column+3] == player_checker:
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for column in range(len(board[0]) - 3):
            if board[row][column] == board[row-1][column+1] == board[row-2][column+2] == board[row-3][column+3] == player_checker:
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the Connect 4 game."""
    board = create_board(ROWS, COLUMNS)
    player_index = get_random_player(PLAYERS)
    player_checker = get_player_checker(player_index)

    while True:
        os.system('clear')
        print_board(board)
        column_index = get_valid_input(player_checker, board)
        place_checker(board, column_index, player_checker)

        if check_win(board, player_checker):
            os.system('clear')
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        player_index = (player_index + 1) % PLAYERS
        player_checker = get_player_checker(player_index)

if __name__ == "__main__":
    game()
