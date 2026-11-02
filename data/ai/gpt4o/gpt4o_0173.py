import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" "] * cols for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(input_char, cols):
    return input_char.isalpha() and 0 <= ord(input_char.upper()) - 65 < cols

def get_next_available_row(board, col):
    for i in range(len(board) - 1, -1, -1):
        if board[i][col] == " ":
            return i
    return None

def place_checker(board, col, checker):
    row = get_next_available_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == checker and all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom left to top right) win
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top left to bottom right) win
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    current_player = random.choice(range(PLAYERS))
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_input = input().strip().upper()
        if is_valid_input(column_input, COLS):
            col = ord(column_input) - 65
            if place_checker(board, col, CHECKERS[current_player]):
                if check_winner(board, CHECKERS[current_player]):
                    print_board(board)
                    print(f"Player {CHECKERS[current_player]} won!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    break
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column is full, turn lost!")
        else:
            print("Invalid input, try again.")

if __name__ == "__main__":
    main()
