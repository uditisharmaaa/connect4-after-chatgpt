import os
import random

# Constants defining the game configuration
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def valid_input(input_str, board):
    if len(input_str) != 1:
        return False
    if input_str not in [chr(65 + i) for i in range(len(board[0]))]:
        return False
    return True

def place_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    # Check horizontal, vertical and diagonal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if check_horizontal(board, row, col, checker) or check_vertical(board, row, col, checker) or check_diagonal(board, row, col, checker):
                return True
    return False

def check_horizontal(board, row, col, checker):
    if col + 3 < NUM_COLS:
        return all(board[row][col + i] == checker for i in range(4))
    return False

def check_vertical(board, row, col, checker):
    if row + 3 < NUM_ROWS:
        return all(board[row + i][col] == checker for i in range(4))
    return False

def check_diagonal(board, row, col, checker):
    if row + 3 < NUM_ROWS and col + 3 < NUM_COLS:
        if all(board[row + i][col + i] == checker for i in range(4)):
            return True
    if row + 3 < NUM_ROWS and col - 3 >= 0:
        if all(board[row + i][col - i] == checker for i in range(4)):
            return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(NUM_COLS))

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_turn = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        print_board(board)
        player_checker = CHECKERS[player_turn]

        column_input = input(f"Player {player_checker}, please enter a column: ").upper()

        while not valid_input(column_input, board) or not place_checker(board, column_input, player_checker):
            column_input = input(f"Invalid input. Player {player_checker}, please enter a column: ").upper()

        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            player_turn = (player_turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
