import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """
    Creates a 2D board with given dimensions, initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    print("  " + " ".join(chr(65 + i) for i in range(NUM_COLS)))
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

def is_valid_input(input_str):
    """
    Checks if the input is a valid column letter.
    """
    if len(input_str)!= 1 or not input_str.isalpha() or not input_str.isupper():
        return False
    col_index = ord(input_str) - ord('A')
    return 0 <= col_index < NUM_COLS

def get_next_player(current_player):
    """
    Returns the next player in the sequence.
    """
    return (current_player + 1) % NUM_PLAYERS

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column, occupying the lowest available space.
    Returns True if the drop was successful, False otherwise.
    """
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    """
    Checks if the given checker has won the game.
    """
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True

    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """
    Checks if the game is a draw (i.e., the board is full).
    """
    return all([cell!= " " for row in board for cell in row])

def game_loop():
    """
    The main game loop.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")

        while True:
            input_str = input().strip()
            if is_valid_input(input_str):
                col = ord(input_str) - ord('A')
                if drop_checker(board, col, players[current_player]):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a column letter (A-{}).".format(chr(65 + NUM_COLS - 1)))

        if check_win(board, players[current_player]):
            os.system('clear')
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = get_next_player(current_player)

if __name__ == "__main__":
    game_loop()
