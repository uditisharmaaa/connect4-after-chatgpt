import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

def place_checker(column, checker, board):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    rows, cols = len(board), len(board[0])
    
    # Check horizontally
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertically
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonally (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Check diagonally (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        print(f"Player {players[current_player]}, it's your turn!")
        column = input("Please enter a column: ").strip().upper()

        while not is_valid_input(column, board):
            print("Invalid input. Try again.")
            column = input("Please enter a column: ").strip().upper()

        place_checker(column, players[current_player], board)
        print_board(board)

        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
