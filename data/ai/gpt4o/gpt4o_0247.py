import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_column(prompt, board):
    while True:
        choice = input(prompt).strip().upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLUMNS - 1):
            col = ord(choice) - 65
            if board[0][col] == " ":
                return col
            else:
                print("Column is full. Try a different one.")
        else:
            print("Invalid input. Enter a single letter for a column within range.")

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):  # Start at bottom row
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_for_winner(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != " ":
                if col <= COLUMNS - 4 and all(board[row][col + offset] == board[row][col] for offset in range(4)):
                    return True
                if row <= ROWS - 4 and all(board[row + offset][col] == board[row][col] for offset in range(4)):
                    return True
                if row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + offset][col + offset] == board[row][col] for offset in range(4)):
                    return True
                if row >= 3 and col <= COLUMNS - 4 and all(board[row - offset][col + offset] == board[row][col] for offset in range(4)):
                    return True
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    player_checkers = CHECKERS[:PLAYERS]

    print_board(board)
    while True:
        prompt = f"Player {player_checkers[current_player]}, please enter a column: "
        col = get_valid_column(prompt, board)
        place_checker(board, col, player_checkers[current_player])

        print_board(board)

        if check_for_winner(board):
            print(f"Player {player_checkers[current_player]} won!")
            break
        if check_for_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
