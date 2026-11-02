import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_input(column_letter):
    return len(column_letter) == 1 and 'A' <= column_letter <= chr(ord('A') + COLS - 1)

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if check_line(board, row, col, 0, 1, checker) or \
               check_line(board, row, col, 1, 0, checker) or \
               check_line(board, row, col, 1, 1, checker) or \
               check_line(board, row, col, 1, -1, checker):
                return True
    return False

def check_line(board, row, col, dr, dc, checker):
    try:
        return all(board[row + i * dr][col + i * dc] == checker for i in range(4))
    except IndexError:  # Trying to access out of board
        return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(range(MAX_PLAYERS))
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        column_letter = input(f"Player {player_checker}, please enter a column: ").upper()

        if not is_valid_input(column_letter):
            print("Invalid input. Try again.")
            continue

        column = ord(column_letter) - ord('A')
        if not place_checker(board, column, player_checker):
            print("Column full. Turn lost.")
            current_player = (current_player + 1) % MAX_PLAYERS
            continue

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
