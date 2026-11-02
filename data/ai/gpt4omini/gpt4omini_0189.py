import random
import os

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col) - 65

def place_checker(board, col, checker):
    col_index = get_column_index(col)
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)) or
                r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)) or
                r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == checker for i in range(4)) or
                r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    players_count = 2
    board = create_board()
    current_player = random.randint(0, players_count - 1)

    print_board(board)
    while True:
        player_checker = PLAYERS[current_player]
        col = input(f"Player {player_checker}, please enter a column: ").upper()

        while not is_valid_input(col) or not place_checker(board, col, player_checker):
            print("Invalid input or column is full. Try again.")
            col = input(f"Player {player_checker}, please enter a column: ").upper()

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % players_count

if __name__ == "__main__":
    main()
