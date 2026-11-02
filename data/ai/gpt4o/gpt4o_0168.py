import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column.isalpha() and 0 <= ord(column) - 65 < COLUMNS

def get_lowest_empty_row(board, column_index):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column_index] == " ":
            return row_index
    return None

def check_for_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col:col + 4] == [checker] * 4:
                return True
    
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal win (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal win (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        user_input = input().strip().upper()
        
        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column_index = ord(user_input) - 65
        row_index = get_lowest_empty_row(board, column_index)

        if row_index is None:
            print(f"Column {user_input} is full. You lose your turn.")
        else:
            board[row_index][column_index] = checker
            print_board(board)
            
            if check_for_win(board, checker):
                print(f"Player {checker} won!")
                break
            
            if check_for_draw(board):
                print("The game is a draw!")
                break
            
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
