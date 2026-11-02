import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = " ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(column_labels)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def select_random_player(players):
    return random.choice(players)

def valid_input(input_str, columns):
    if len(input_str) != 1:  # Only single character inputs are valid
        return False
    if input_str < 'A' or input_str > chr(ord('A') + columns - 1):  # Input should be within column range
        return False
    return True

def place_checker(board, column, checker): 
    for row in reversed(board):  # Start from bottom of the column
        if row[column] == ' ':
            row[column] = checker
            return
    raise ValueError("Column is already full")

def check_winner(board, checker):
    rows = len(board)
    columns = len(board[0])

    for r in range(rows):
        for c in range(columns):
            if board[r][c] != checker:
                continue

            # Check horizontally
            if c + 3 < columns and all(board[r][c + i] == checker for i in range(4)):
                return True

            # Check vertically
            if r + 3 < rows and all(board[r + i][c] == checker for i in range(4)):
                return True

            # Check diagonal (\ direction)
            if r + 3 < rows and c + 3 < columns and all(board[r + i][c + i] == checker for i in range(4)):
                return True

            # Check diagonal (/ direction)
            if r - 3 >= 0 and c + 3 < columns and all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = CHECKERS.index(select_random_player(CHECKERS))

    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_idx]
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()

        if valid_input(user_input, COLUMNS):
            try:
                column_idx = ord(user_input) - ord('A')
                place_checker(board, column_idx, current_checker)
            except ValueError:
                print("Column is full, turn is invalid.")
                current_player_idx = (current_player_idx + 1) % PLAYERS  # Skip turn
            else:
                print_board(board)

                if check_winner(board, current_checker):
                    print(f"Player {current_checker} won!")
                    break

                if check_draw(board):
                    print("The game is a draw.")
                    break

            current_player_idx = (current_player_idx + 1) % PLAYERS  # Next turn
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
