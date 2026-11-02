import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_COUNT = 2

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_char):
    return input_char.isalpha() and 'A' <= input_char <= chr(65 + COLUMNS - 1)

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
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
    # Check diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    print_board(board)
    
    players_checkers = CHECKERS[:PLAYER_COUNT]
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    
    while True:
        current_checker = players_checkers[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        player_input = input().strip().upper()
        
        if not is_valid_input(player_input):
            print("Invalid input. Please enter a valid column.")
            continue
        
        column = ord(player_input) - 65
        
        if not place_checker(board, column, current_checker):
            print("Column is full. You lose your turn.")
        else:
            print_board(board)
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
