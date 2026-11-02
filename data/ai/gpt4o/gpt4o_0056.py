import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column():
    while True:
        column = input("Please enter a column: ").upper()
        if column in COLUMN_LABELS:
            return COLUMN_LABELS.index(column)
        else:
            print("Invalid input. Please enter a valid column label.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal check (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Diagonal check (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn.")
        
        column_index = get_valid_column()

        if not place_checker(board, column_index, current_player):
            print("Column is full. Turn lost.")
            current_player_index = (current_player_index + 1) % len(PLAYERS)
            continue

        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

connect4()
