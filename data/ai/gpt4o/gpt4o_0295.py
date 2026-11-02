import os
import random

# Constants for game setup
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2  # This can be set to 2-5
CHECKERS = ["X", "O", "V", "H", "M"]
CHECKERS = CHECKERS[:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column):
    if len(column) == 1 and column.isalpha():
        col_index = ord(column) - ord('A')
        return 0 <= col_index < COLUMNS
    return False

def get_column_index(column):
    return ord(column) - ord('A')

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col+4] == [checker] * 4:
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom left to top right)
    for col in range(COLUMNS - 3):
        for row in range(ROWS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for col in range(COLUMNS - 3):
        for row in range(3, ROWS):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_connect4():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        user_input = input().strip().upper()
        
        if not is_valid_input(user_input):
            print("Invalid input. Please enter a column letter (e.g., A, B, C).")
            continue
        
        column_index = get_column_index(user_input)
        
        if not place_checker(board, column_index, current_checker):
            print("Column full. Try a different column.")
            continue
        
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    play_connect4()
