import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS))
    print(column_labels)
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(input_str, columns):
    return len(input_str) == 1 and input_str.isalpha() and ord(input_str) - ord('A') in range(columns)

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right & up-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = MIN_PLAYERS  # Set number of players to 2 for submission
    player_checkers = CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        print(f"Player {player_checkers[current_player]}, please enter a column:")
        player_input = input().strip().upper()

        if not is_valid_input(player_input, COLUMNS):
            print("Invalid input, please try again.")
            continue
        
        column = ord(player_input) - ord('A')
        if not place_checker(board, column, player_checkers[current_player]):
            print("Column full, please choose another column.")
            continue

        print_board(board)

        if check_win(board, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
