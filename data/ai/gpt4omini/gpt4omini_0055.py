import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col_input):
    if len(col_input) != 1:
        return False
    if col_input not in [chr(65 + i) for i in range(COLS)]:
        return False
    return True

def get_column_index(col_input):
    return ord(col_input) - 65

def place_checker(board, col_index, checker):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False 

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS[:2])  # Randomly select first player
    print_board(board)

    turn = 0
    while True:
        current_checker = PLAYERS[turn % len(PLAYERS)]
        valid_input = False
        
        while not valid_input:
            col_input = input(f"Player {current_checker}, please enter a column: ").upper()
            if is_valid_input(col_input):
                col_index = get_column_index(col_input)
                valid_input = place_checker(board, col_index, current_checker)
                if not valid_input:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please try again.")

        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        turn += 1

if __name__ == "__main__":
    main()
