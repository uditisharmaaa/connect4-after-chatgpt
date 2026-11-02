import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Only the first PLAYER_COUNT will be used

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    col_labels = "   ".join(chr(65 + i) for i in range(COLUMNS))
    print("  " + col_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_input():
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLUMNS - 1):
            return ord(user_input) - 65
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonals
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_four(board, row, col, checker):
                return True
    return False

def check_four(board, row, col, checker):
    # Conditions to check horizontal, vertical, and diagonal wins
    if (
        col + 3 < COLUMNS and
        all(board[row][col+i] == checker for i in range(4))
    ):
        return True
    if (
        row + 3 < ROWS and
        all(board[row+i][col] == checker for i in range(4))
    ):
        return True
    if (
        row + 3 < ROWS and col + 3 < COLUMNS and
        all(board[row+i][col+i] == checker for i in range(4))
    ):
        return True
    if (
        row - 3 >= 0 and col + 3 < COLUMNS and
        all(board[row-i][col+i] == checker for i in range(4))
    ):
        return True
    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)
    print(f"Player {CHECKERS[current_player]}, it's your turn.")
    
    while True:
        col = get_valid_input()
        if place_checker(board, col, CHECKERS[current_player]):
            print_board(board)

            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYER_COUNT
            print(f"Player {CHECKERS[current_player]}, it's your turn.")
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    play_game()
