import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * NUM_COLS)
        print("|   " * NUM_COLS)
        for cell in row:
            print("| " + cell + " ", end="")
        print("|")
        print("+---" * NUM_COLS)

def get_player_checker(player_index):
    """Get the checker for the current player"""
    return CHECKERS[player_index % NUM_PLAYERS]

def is_valid_input(input_str):
    """Check if the user input is valid"""
    return input_str.upper() >= "A" and input_str.upper() <= chr(ord("A") + NUM_COLS - 1)

def get_column_index(input_str):
    """Get the column index from the user input"""
    return ord(input_str.upper()) - ord("A")

def drop_checker(board, column_index, checker):
    """Drop the checker into the column"""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_win(board):
    """Check if there is a winner"""
    for row in board:
        for col in range(NUM_COLS - 3):
            if row[col]!= " " and row[col] == row[col+1] == row[col+2] == row[col+3]:
                return row[col]
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col]!= " " and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return board[row][col]
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col]!= " " and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return board[row][col]
            if board[row][col+3]!= " " and board[row][col+3] == board[row+1][col+2] == board[row+2][col+1] == board[row+3][col]:
                return board[row][col+3]
    return None

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= " " for row in board for cell in row)

def main():
    board = create_board()
    player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        checker = get_player_checker(player_index)
        input_str = input("Player {}, please enter a column: ".format(checker))
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue
        column_index = get_column_index(input_str)
        if all(cell!= " " for cell in [row[column_index] for row in board]):
            print("Column is full. Please try again.")
            continue
        drop_checker(board, column_index, checker)
        winner = check_win(board)
        if winner is not None:
            print_board(board)
            print("Player {} won!".format(winner))
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        player_index = (player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
