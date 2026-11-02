import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # For up to 5 players

def print_board(board):
    os.system('clear')  # Clears the screen
    print("  " + "   ".join([chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def is_valid_move(board, column):
    return column in range(COLUMNS) and board[0][column] == " "

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_for_win(board, checker):
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

    # Check diagonal (bottom left to top right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def connect4():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    checker = CHECKERS[current_player]
    
    print_board(board)

    while True:
        column_choice = input(f"Player {checker}, please enter a column: ").upper()

        if len(column_choice) != 1 or not column_choice.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column = ord(column_choice) - ord('A')

        if not is_valid_move(board, column):
            print("Invalid move. Please choose another column.")
            continue

        place_checker(board, column, checker)
        print_board(board)

        if check_for_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break

        # Alternate to the next player
        current_player = (current_player + 1) % PLAYERS
        checker = CHECKERS[current_player]

# Run the game with 6x7 dimensions and 2 players
connect4()
