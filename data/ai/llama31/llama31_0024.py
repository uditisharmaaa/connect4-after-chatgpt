import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with whitespaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---+---+---+---+---+---+---+")

def get_player_move(player):
    """Get a valid move from the player."""
    while True:
        move = input(f"Player {player}, please enter a column: ")
        if move.upper() in "ABCDEFG":
            if ord(move.upper()) - ord('A') < BOARD_COLS:
                return ord(move.upper()) - ord('A')
        print("Invalid input. Please try again.")

def drop_checker(board, col, player):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        move = get_player_move(current_player)
        drop_checker(board, move, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
