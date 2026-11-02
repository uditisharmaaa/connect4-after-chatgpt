import os
import random

# Global constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(width, height):
    """Create a 2D board with the given width and height."""
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board

def print_board(board):
    """Print the current state of the board."""
    print("  A B C D E F G")
    for row in board:
        print("+---" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+---" * len(row))

def get_player_checker(player_index):
    """Get the checker symbol for the given player index."""
    return CHECKERS[player_index]

def is_valid_input(column):
    """Check if the input column is valid."""
    return column.upper() >= "A" and column.upper() <= chr(ord("A") + BOARD_WIDTH - 1)

def get_column_index(column):
    """Get the column index from the input column letter."""
    return ord(column.upper()) - ord("A")

def is_column_full(board, column_index):
    """Check if the column is full."""
    return board[0][column_index]!= " "

def get_next_empty_row(board, column_index):
    """Get the next empty row in the column."""
    for row_index in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row_index][column_index] == " ":
            return row_index
    return None

def place_checker(board, column_index, checker):
    """Place the checker in the column."""
    row_index = get_next_empty_row(board, column_index)
    if row_index is not None:
        board[row_index][column_index] = checker
    else:
        print("Column is full. Please try again.")

def check_win(board, checker):
    """Check if the player has won."""
    # Check horizontal wins
    for row in board:
        for col in range(BOARD_WIDTH - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical wins
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for col in row:
            if col == " ":
                return False
    return True

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(players[current_player_index])}, please enter a column:")

        while True:
            column = input().strip()
            if is_valid_input(column):
                column_index = get_column_index(column)
                if not is_column_full(board, column_index):
                    break
                else:
                    print("Column is full. Please try again.")
            else:
                print("Invalid input. Please try again.")

        place_checker(board, column_index, get_player_checker(players[current_player_index]))

        if check_win(board, get_player_checker(players[current_player_index])):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(players[current_player_index])} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
