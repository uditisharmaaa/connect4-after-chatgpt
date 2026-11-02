import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY_CELL = ' '

# Initialize board
def initialize_board():
    return [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

# Get valid input
def get_valid_input():
    while True:
        col = input("Enter column: ").strip().upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1):
            return ord(col) - 65
        print("Invalid input. Try again.")

# Place checker
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = checker
            return True
    return False

# Check win
def check_win(board, checker):
    def check_direction(dx, dy):
        for x in range(ROWS):
            for y in range(COLS):
                if all(
                    0 <= x + i * dx < ROWS and
                    0 <= y + i * dy < COLS and
                    board[x + i * dx][y + i * dy] == checker
                    for i in range(4)
                ):
                    return True

    return any(check_direction(*direction) for direction in [(0, 1), (1, 0), (1, 1), (1, -1)])

# Check draw
def check_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

def main():
    board = initialize_board()
    players = CHECKERS[:MAX_PLAYERS]
    current_player = random.choice(players)

    print_board(board)
    while True:
        print(f"Player {current_player}, it's your turn.")
        col = get_valid_input()

        if not place_checker(board, col, current_player):
            print("Column is full, you lose your turn.")
        else:
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break

            current_player = players[(players.index(current_player) + 1) % MAX_PLAYERS]

if __name__ == "__main__":
    main()
