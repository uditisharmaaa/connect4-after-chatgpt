import os
import random

# Constants for the game
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LETTERS = [chr(i) for i in range(65, 65 + NUM_COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_LETTERS))
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

def select_random_player():
    return random.randint(0, NUM_PLAYERS - 1)

def get_column_index(column_letter):
    if column_letter in COLUMN_LETTERS:
        return COLUMN_LETTERS.index(column_letter)
    return -1

def is_valid_move(board, column_index):
    return board[0][column_index] == " "

def place_checker(board, column_index, checker):
    for i in reversed(range(NUM_ROWS)):
        if board[i][column_index] == " ":
            board[i][column_index] = checker
            return

def check_winner(board):
    # Horizontal check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != " " and all(board[row][col + i] == board[row][col] for i in range(4)):
                return True
    # Vertical check
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] != " " and all(board[row + i][col] == board[row][col] for i in range(4)):
                return True
    # Diagonal check (bottom left to top right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != " " and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                return True
    # Diagonal check (bottom right to top left)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != " " and all(board[row - i][col + i] == board[row][col] for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(NUM_COLUMNS))

def play_game():
    board = create_board()
    current_player = select_random_player()
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        column_letter = input(f"Player {checker}, please enter a column: ").upper()
        
        column_index = get_column_index(column_letter)
        if column_index == -1 or not is_valid_move(board, column_index):
            print("Invalid move. Try again.")
            continue

        place_checker(board, column_index, checker)
        print_board(board)

        if check_winner(board):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
