import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = [chr(65 + i) for i in range(len(board[0]))]
    print("  " + "   ".join(column_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(user_input, board):
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    column_index = ord(user_input.upper()) - 65
    return 0 <= column_index < len(board[0]) and board[0][column_index] == " "

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals (/ direction)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonals (\ direction)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Set up the board and players
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:2]  # Default to 2 players
    random.shuffle(players)
    turn = 0

    print_board(board)
    print(f"Player {players[turn]}, you go first!")

    while True:
        player = players[turn]
        user_input = input(f"Player {player}, please enter a column: ").upper()

        if not is_valid_input(user_input, board):
            print("Invalid input. Please try again.")
            continue

        column_index = ord(user_input) - 65
        place_checker(board, column_index, player)
        print_board(board)

        if check_winner(board, player):
            print(f"Player {player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
