import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # Expandable for more players

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # For Linux/Unix
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A-G
    print("+---" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLUMNS)

def is_valid_input(col):
    return col in range(COLUMNS)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    while not game_over:
        print_board(board)
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if col_input in [chr(65 + i) for i in range(COLUMNS)]:
            col = ord(col_input) - 65
            if is_valid_input(col) and drop_checker(board, col, current_player):
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    game_over = True
                elif is_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    game_over = True
                else:
                    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            else:
                print("Column is full, please choose another.")
        else:
            print("Invalid input, please enter a letter from A to G.")
        
if __name__ == "__main__":
    main()
