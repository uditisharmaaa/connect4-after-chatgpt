import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Creates an empty game board with the specified number of rows and columns."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Prints the game board with column labels."""
    print('  ' + '   '.join(chr(65 + i) for i in range(cols)))
    print('+---' * cols + '+')
    for row in board:
        print('|   ' * cols + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * cols + '+')
    print()

def get_valid_input(player, cols):
    """Gets a valid column input from the user."""
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(65 + cols - 1):
            return ord(user_input) - 65
        print("Invalid input. Please enter a letter between A and", chr(65 + cols - 1))

def drop_checker(board, col, player):
    """Drops a checker into the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break
    else:
        print("Column is full. Turn lost.")
        return False
    return True

def check_win(board, player):
    """Checks if the specified player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == player:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Plays a game of Connect 4."""
    num_players = 2  # Set the number of players to 2
    players = CHECKERS[:num_players]
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board, BOARD_COLS)
        col = get_valid_input(current_player, BOARD_COLS)
        if drop_checker(board, col, current_player):
            if check_win(board, current_player):
                os.system('clear')
                print_board(board, BOARD_COLS)
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                os.system('clear')
                print_board(board, BOARD_COLS)
                print("It's a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    game()
