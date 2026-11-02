import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(c) for c in range(65, 65 + COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_column(column):
    return column.isalpha() and 'A' <= column <= chr(65 + COLUMNS - 1)

def get_next_open_row(board, col_index):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            return row
    return None

def place_checker(board, col_index, checker):
    row = get_next_open_row(board, col_index)
    if row is not None:
        board[row][col_index] = checker
        return True
    return False

def check_for_win(board, checker):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Positive Diagonal Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Negative Diagonal Check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player]
        column = input(f"Player {player_checker}, please enter a column: ")
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(column.upper()) - 65
        
        if place_checker(board, col_index, player_checker):
            print_board(board)
            if check_for_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            if check_for_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. Try another column.")

if __name__ == "__main__":
    main()
