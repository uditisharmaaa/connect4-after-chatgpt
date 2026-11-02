import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with the given dimensions"""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print("  A B C D E F G")
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_input(input_str, cols):
    """Check if the input is a valid column letter"""
    return input_str.isalpha() and len(input_str) == 1 and ord(input_str.upper()) - ord('A') < cols

def get_player_input(player, board):
    """Get the player's input and validate it"""
    while True:
        input_str = input(f"Player {player}, please enter a column: ")
        if is_valid_input(input_str, COLS):
            col_idx = ord(input_str.upper()) - ord('A')
            if board[0][col_idx]!= " ":
                print("Column is full, please choose another column.")
                continue
            return col_idx
        print("Invalid input, please enter a letter from A to G.")

def drop_checker(board, player, col_idx):
    """Drop the player's checker into the given column"""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player
            break

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal wins
    for row_idx in range(ROWS):
        for col_idx in range(COLS - 3):
            if board[row_idx][col_idx] == player and board[row_idx][col_idx + 1] == player and board[row_idx][col_idx + 2] == player and board[row_idx][col_idx + 3] == player:
                return True

    # Check vertical wins
    for row_idx in range(ROWS - 3):
        for col_idx in range(COLS):
            if board[row_idx][col_idx] == player and board[row_idx + 1][col_idx] == player and board[row_idx + 2][col_idx] == player and board[row_idx + 3][col_idx] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row_idx in range(ROWS - 3):
        for col_idx in range(COLS - 3):
            if board[row_idx][col_idx] == player and board[row_idx + 1][col_idx + 1] == player and board[row_idx + 2][col_idx + 2] == player and board[row_idx + 3][col_idx + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row_idx in range(3, ROWS):
        for col_idx in range(COLS - 3):
            if board[row_idx][col_idx] == player and board[row_idx - 1][col_idx + 1] == player and board[row_idx - 2][col_idx + 2] == player and board[row_idx - 3][col_idx + 3] == player:
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
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    while True:
        os.system('clear')
        print_board(board)
        player = players[current_player_idx]
        col_idx = get_player_input(player, board)
        drop_checker(board, player, col_idx)
        if check_win(board, player):
            os.system('clear')
            print_board(board)
            print(f"Player {player} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
