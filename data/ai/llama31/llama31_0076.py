import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")
    print("Player " + players[0] + ", please enter a column: ")

def get_valid_input():
    """Get a valid input from the user."""
    while True:
        col = input().upper()
        if col in string.ascii_uppercase[:BOARD_COLS]:
            return ord(col) - ord('A')
        print("Invalid input. Please enter a letter between A and", chr(ord('A') + BOARD_COLS - 1))

def is_valid_move(board, col):
    """Check if a move is valid."""
    return board[0][col] == " "

def make_move(board, player, col):
    """Make a move on the board."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            break

def check_win(board, player):
    """Check if a player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True
    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
            if board[row][col+3] == player and board[row+1][col+2] == player and board[row+2][col+1] == player and board[row+3][col] == player:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(all(cell!= " " for cell in row) for row in board)

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)
    board = create_board()
    print_board(board, players)
    while True:
        col = get_valid_input()
        if not is_valid_move(board, col):
            print("Invalid move. Column is full.")
            continue
        make_move(board, current_player, col)
        print_board(board, players)
        if check_win(board, current_player):
            print("Player", current_player, "won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
