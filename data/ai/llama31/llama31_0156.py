import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with whitespaces"""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print("  " + " ".join(chr(65 + i) for i in range(BOARD_COLS)))
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def is_valid_input(column):
    """Check if the user input is a valid column letter"""
    return column.isalpha() and len(column) == 1 and ord(column) - 65 < BOARD_COLS

def get_player_move(player, board):
    """Get the player's move (column letter) and validate it"""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if is_valid_input(column):
            return ord(column) - 65
        print("Invalid input. Please enter a letter between A and", chr(65 + BOARD_COLS - 1))

def drop_checker(board, column, player):
    """Drop the checker into the specified column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return

def check_win(board, player):
    """Check if the player has won by having 4 checkers in a row"""
    # Check horizontal
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (no more empty spaces)"""
    return all(all(cell!= " " for cell in row) for row in board)

def game():
    """Main game loop"""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        column = get_player_move(current_player, board)
        drop_checker(board, column, current_player)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

game()
