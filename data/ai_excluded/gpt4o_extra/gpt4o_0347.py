import os
import random

# Constants for game setup
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    column_labels = "  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS))
    print(column_labels)
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(user_input):
    return user_input.isalpha() and len(user_input) == 1 and 65 <= ord(user_input) < 65 + COLUMNS

def get_column_index(user_input):
    return ord(user_input) - 65

def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

def check_win(board, symbol):
    # Check horizontal locations
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    # Check vertical locations
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    num_players = 2  # Use a constant or variable to choose the number of players
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G):")
        user_input = input().strip().upper()

        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column_index = get_column_index(user_input)

        if not place_checker(board, column_index, current_player):
            print(f"Column {user_input} is full. Try another column.")
            continue

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
