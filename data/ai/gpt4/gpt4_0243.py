import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(column, columns):
    return column.isalpha() and len(column) == 1 and 0 <= ord(column.upper()) - 65 < columns

def get_valid_input(prompt, columns):
    while True:
        column = input(prompt).upper()
        if is_valid_input(column, columns):
            return ord(column) - 65
        else:
            print("Invalid input. Please select a valid column.")

def is_column_full(board, column_number):
    return board[0][column_number] != ' '

def place_checker(board, column_number, checker):
    for row in reversed(board):
        if row[column_number] == ' ':
            row[column_number] = checker
            break

def check_winner(board, checker, rows, columns):
    # Check horizontal
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board, rows, columns):
    return all(board[0][col] != ' ' for col in range(columns))

def main():
    # Game settings
    num_players = 2  # Default to 2 players
    assert 2 <= num_players <= MAX_PLAYERS, "Number of players must be between 2 and 5."
    
    player_checkers = PLAYER_CHECKERS[:num_players]
    board = create_board(ROWS, COLUMNS)

    # Randomize starting player
    current_player_index = random.randint(0, num_players - 1)

    # Main game loop
    while True:
        print_board(board)
        current_player_checker = player_checkers[current_player_index]

        print(f"Player {current_player_checker}, it's your turn!")
        column = get_valid_input("Please enter a column (A-G): ", COLUMNS)

        if is_column_full(board, column):
            print(f"Column {chr(65 + column)} is full! Turn lost.")
        else:
            place_checker(board, column, current_player_checker)
            if check_winner(board, current_player_checker, ROWS, COLUMNS):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                break
            if check_draw(board, ROWS, COLUMNS):
                print_board(board)
                print("It's a draw!")
                break

            # Switch to next player
            current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
