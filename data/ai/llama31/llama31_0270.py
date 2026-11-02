import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+" * NUM_COLS)
        print("| {} |".format(" | ".join(row)))
    print("+---+" * NUM_COLS)

def get_player_checker(player_num):
    """Return the checker for the given player number"""
    return CHECKERS[player_num - 1]

def is_valid_input(column):
    """Check if the input column is valid"""
    return column.upper() >= "A" and column.upper() <= chr(64 + NUM_COLS)

def get_next_open_row(board, column):
    """Get the next open row in the given column"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1

def drop_checker(board, column, checker):
    """Drop the checker in the given column"""
    row = get_next_open_row(board, column)
    if row == -1:
        return False
    board[row][column] = checker
    return True

def check_win(board, checker):
    """Check if the given player has won"""
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = players.pop(0)

    while True:
        os.system('clear')
        print_board(board)
        print("Player {}, please enter a column:".format(get_player_checker(current_player)))

        while True:
            column = input()
            if is_valid_input(column):
                column = ord(column.upper()) - 65
                if drop_checker(board, column, get_player_checker(current_player)):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a column between A and {}.".format(chr(64 + NUM_COLS)))

        if check_win(board, get_player_checker(current_player)):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(get_player_checker(current_player)))
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        players.append(players.pop(players.index(current_player)))
        current_player = players[0]

if __name__ == "__main__":
    main()
