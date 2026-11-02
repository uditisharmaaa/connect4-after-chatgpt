import os
import random

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_CHECKERS_TO_WIN = 4

def create_board():
    """Create an empty board with whitespaces."""
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

def get_player_checker(player_index):
    """Get the checker for a specific player."""
    return CHECKERS[player_index]

def get_player_input(player_index, board):
    """Get the player's column choice and validate it."""
    while True:
        column_choice = input(f"Player {get_player_checker(player_index)}, please enter a column: ")
        if column_choice.upper() < 'A' or column_choice.upper() > chr(64 + NUM_COLS):
            print("Invalid column. Please enter a letter between A and", chr(64 + NUM_COLS))
        elif board[NUM_ROWS - 1][ord(column_choice.upper()) - 65]!= " ":
            print("Column is full. Please choose another column.")
        else:
            return ord(column_choice.upper()) - 65

def place_checker(board, player_index, column):
    """Place a checker in the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = get_player_checker(player_index)
            break

def check_win(board, player_index):
    """Check if a player has won."""
    checker = get_player_checker(player_index)
    # Check horizontal locations for win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - MAX_CHECKERS_TO_WIN + 1):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical locations for win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - MAX_CHECKERS_TO_WIN + 1):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check positively sloped diagonals
    for row in range(NUM_ROWS - MAX_CHECKERS_TO_WIN + 1):
        for col in range(NUM_COLS - MAX_CHECKERS_TO_WIN + 1):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check negatively sloped diagonals
    for row in range(MAX_CHECKERS_TO_WIN - 1, NUM_ROWS):
        for col in range(NUM_COLS - MAX_CHECKERS_TO_WIN + 1):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def main():
    board = create_board()
    player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        column = get_player_input(player_index, board)
        place_checker(board, player_index, column)
        if check_win(board, player_index):
            print_board(board)
            print("Player", get_player_checker(player_index), "won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        player_index = (player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
