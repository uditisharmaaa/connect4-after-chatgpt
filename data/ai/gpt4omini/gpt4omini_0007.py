import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---+" + "---+" * (COLUMNS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLUMNS - 1))

def is_valid_input(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != ' ':
        return False
    return True

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G):")
        user_input = input().strip().upper()

        if len(user_input) != 1 or not user_input.isalpha():
            continue  # Invalid input, ask again

        column = ord(user_input) - 65  # Convert letter to column index

        if is_valid_input(column, board):
            place_checker(board, column, current_player)

            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            # Alternate players
            current_player = PLAYERS[0] if current_player == PLAYERS[1] else PLAYERS[1]
        else:
            continue  # Invalid column, ask again

if __name__ == "__main__":
    main()
