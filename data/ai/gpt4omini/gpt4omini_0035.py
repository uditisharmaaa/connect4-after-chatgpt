import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i + 65) for i in range(COLS)))
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(col, board):
    if col < 0 or col >= COLS or board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and all(board[row][col + i] == checker for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4))) or \
               (row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4))) or \
               (row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_checker = PLAYERS[current_player_index]
        col_input = input(f"Player {current_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        if col_input not in [chr(i) for i in range(65, 65 + COLS)]:
            print("Invalid input. Please enter a valid column.")
            continue

        col = ord(col_input) - 65

        if not is_valid_input(col, board):
            print("Column is full or invalid. Please try again.")
            continue

        place_checker(board, col, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
