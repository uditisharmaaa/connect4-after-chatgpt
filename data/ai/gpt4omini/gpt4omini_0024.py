import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def random_first_player(num_players):
    return random.randint(0, num_players - 1)

def get_column_choice(player):
    while True:
        choice = input(f"Player {CHECKERS[player]}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLS - 1):
            return ord(choice) - 65
        print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):  # Horizontal
                return True
            if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):  # Vertical
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):  # Diagonal \
                return True
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):  # Diagonal /
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    num_players = 2  # You can set this to any value between 2 and MAX_PLAYERS
    current_player = random_first_player(num_players)

    print_board(board)

    while True:
        column = get_column_choice(current_player)

        if place_checker(board, column, CHECKERS[current_player]):
            print_board(board)

            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % num_players
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
