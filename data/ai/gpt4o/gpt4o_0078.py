import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_choice(choice):
    return choice in COLUMN_LABELS

def place_checker(board, column, checker):
    col = COLUMN_LABELS.index(column)
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (down-right) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (up-right) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = create_board()
    print_board(board)

    players = CHECKERS[:PLAYERS_COUNT]
    current_player = random.choice(players)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        choice = input().strip().upper()
        
        if not is_valid_choice(choice):
            print("Invalid column. Please choose a valid column.")
            continue
        
        if not place_checker(board, choice, current_player):
            print("Column full. Turn is lost.")
            current_player = players[(players.index(current_player) + 1) % PLAYERS_COUNT]
            continue
        
        print_board(board)
        
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player = players[(players.index(current_player) + 1) % PLAYERS_COUNT]

if __name__ == "__main__":
    play_game()
