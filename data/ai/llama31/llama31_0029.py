import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS_CHECKERS = CHECKERS[:NUM_PLAYERS]

def create_board():
    """Create an empty board."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_num):
    """Get the checker for the current player."""
    return PLAYERS_CHECKERS[player_num]

def get_player_move(player_num):
    """Get the move from the current player."""
    while True:
        move = input("Player {}, please enter a column: ".format(get_player_checker(player_num)))
        if move.upper() in string.ascii_uppercase[:BOARD_COLS]:
            return move.upper()
        print("Invalid input. Please enter a letter from A to {}.".format(chr(64 + BOARD_COLS)))

def make_move(board, player_num, move):
    """Make a move on the board."""
    col = ord(move) - 65
    for row in reversed(board):
        if row[col] == " ":
            row[col] = get_player_checker(player_num)
            return True
    print("Column is full. Please try again.")
    return False

def check_win(board, player_num):
    """Check if the current player has won."""
    checker = get_player_checker(player_num)
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([row[col] == checker for row in board[i:i+4]]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all([all([cell!= " " for cell in row]) for row in board])

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        move = get_player_move(current_player)
        if make_move(board, current_player, move):
            if check_win(board, current_player):
                print_board(board)
                print("Player {} won!".format(get_player_checker(current_player)))
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
