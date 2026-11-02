import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D board with whitespaces."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the board to the console."""
    column_labels = [string.ascii_uppercase[i] for i in range(BOARD_WIDTH)]
    print('  ' + '   '.join(column_labels))
    print('+---' * BOARD_WIDTH + '+')
    for row in board:
        print('|   ' * BOARD_WIDTH + '|')
        print('+---' * BOARD_WIDTH + '+')

def validate_input(column, width):
    """Validate user input."""
    if not column.isalpha():
        return False
    column = ord(column.upper()) - ord('A')
    return 0 <= column < width

def get_player_move(player, width):
    """Get player move and validate input."""
    while True:
        column = input(f"Player {player}, please enter a column: ")
        if validate_input(column, width):
            return column.upper()
        print("Invalid input. Please enter a letter between A and", string.ascii_uppercase[width-1])

def place_checker(board, column, player):
    """Place a checker in the specified column."""
    column = ord(column) - ord('A')
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return

def check_win(board, player):
    """Check for a win."""
    # Check horizontal locations for win
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == player and row[col+1] == player and row[col+2] == player and row[col+3] == player:
                return True

    # Check vertical locations for win
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

def check_draw(board):
    """Check for a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    num_players = 2  # Set to 2 players
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)

    while True:
        os.system('clear')
        print_board(board)

        current_player = players[current_player_index]
        column = get_player_move(current_player, BOARD_WIDTH)
        place_checker(board, column, current_player)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
