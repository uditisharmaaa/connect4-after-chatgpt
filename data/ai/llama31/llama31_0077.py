import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the given dimensions."""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board, player_turn):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")
    print("Player {}, please enter a column:".format(PLAYERS[player_turn]))

def validate_input(board, column):
    """Check if the input is a valid column and not full."""
    if not column.isalpha() or not column.upper() in "ABCDEFG":
        return False
    column_index = ord(column.upper()) - ord('A')
    return board[0][column_index] == " "

def place_checker(board, column, player):
    """Place a checker in the given column."""
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = PLAYERS[player]
            return

def check_win(board, player):
    """Check for a win in all directions."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == PLAYERS[player]:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == PLAYERS[player]:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == PLAYERS[player]:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == PLAYERS[player]:
                return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell!= " " for row in board for cell in row)

def main():
    board = create_board()
    num_players = 2
    player_turn = random.randint(0, num_players - 1)
    while True:
        print_board(board, player_turn)
        column = input().upper()
        while not validate_input(board, column):
            print("Invalid input, please try again.")
            column = input().upper()
        place_checker(board, column, player_turn)
        if check_win(board, player_turn):
            print_board(board, player_turn)
            print("Player {} won!".format(PLAYERS[player_turn]))
            break
        if check_draw(board):
            print_board(board, player_turn)
            print("It's a draw!")
            break
        player_turn = (player_turn + 1) % num_players

if __name__ == "__main__":
    main()
