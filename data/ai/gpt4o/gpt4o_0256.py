import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(choice, columns):
    return choice.isalpha() and len(choice) == 1 and 'A' <= choice.upper() < chr(ord('A') + columns)

def get_column_number(choice):
    return ord(choice.upper()) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal win conditions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col + i] == checker for i in range(4))) or \
               (row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4))) or \
               (col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == checker for i in range(4))) or \
               (col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    current_player = random.randint(0, PLAYERS - 1)
    player_count = PLAYERS
    game_over = False

    while not game_over:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        choice = input().strip()

        if not is_valid_column(choice, COLUMNS):
            print("Invalid input. Try again.")
            continue

        col = get_column_number(choice)
        
        if is_column_full(board, col):
            print("Column full. Turn lost.")
            current_player = (current_player + 1) % player_count
            continue

        drop_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
