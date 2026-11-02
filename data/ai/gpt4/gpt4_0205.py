import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # For up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_index(column):
    if len(column) == 1 and "A" <= column <= chr(64 + COLUMNS):
        return ord(column) - 65
    return -1

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):  # Horizontal
                return True
            if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):    # Vertical
                return True
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):  # Diagonal /
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):       # Diagonal \
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    players_checkers = CHECKERS[:PLAYERS]

    print_board(board)
    
    while True:
        print(f"Player {players_checkers[current_player]}, please enter a column:")
        column = input().strip().upper()
        column_index = get_column_index(column)
        
        if column_index == -1:
            print("Invalid input. Try again.")
            continue

        if not place_checker(board, column_index, players_checkers[current_player]):
            print("Column full. Try again.")
            continue

        print_board(board)

        if check_win(board, players_checkers[current_player]):
            print(f"Player {players_checkers[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
