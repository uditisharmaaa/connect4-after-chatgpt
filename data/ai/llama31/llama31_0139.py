import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized with whitespaces"""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    col_index = ord(input_str.upper()) - ord('A')
    return 0 <= col_index < BOARD_COLS

def get_player_input(player):
    """Get the player's input and validate it"""
    while True:
        input_str = input("Player {}, please enter a column: ".format(player))
        if is_valid_input(input_str):
            return ord(input_str.upper()) - ord('A')
        print("Invalid input. Please try again.")

def drop_checker(board, player, col_index):
    """Drop the checker into the specified column"""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player
            break

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal locations for win
    for row in board:
        for col_index in range(BOARD_COLS - 3):
            if row[col_index] == player and row[col_index + 1] == player and row[col_index + 2] == player and row[col_index + 3] == player:
                return True

    # Check vertical locations for win
    for col_index in range(BOARD_COLS):
        for row_index in range(BOARD_ROWS - 3):
            if board[row_index][col_index] == player and board[row_index + 1][col_index] == player and board[row_index + 2][col_index] == player and board[row_index + 3][col_index] == player:
                return True

    # Check positively sloped diagonals
    for row_index in range(BOARD_ROWS - 3):
        for col_index in range(BOARD_COLS - 3):
            if board[row_index][col_index] == player and board[row_index + 1][col_index + 1] == player and board[row_index + 2][col_index + 2] == player and board[row_index + 3][col_index + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row_index in range(3, BOARD_ROWS):
        for col_index in range(BOARD_COLS - 3):
            if board[row_index][col_index] == player and board[row_index - 1][col_index + 1] == player and board[row_index - 2][col_index + 2] == player and board[row_index - 3][col_index + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Create the board and select the first player
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board)
        current_player = players[current_player_index]
        col_index = get_player_input(current_player)
        drop_checker(board, current_player, col_index)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(current_player))
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
