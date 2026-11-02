import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_column(column):
    return len(column) == 1 and column.isalpha() and "A" <= column <= chr(65 + COLS - 1)

def get_column_index(letter):
    return ord(letter) - 65

def place_checker(board, column, checker):
    col_idx = get_column_index(column)
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and col >= 3 and all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    clear_screen()
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid input, try again.")
            continue
        
        if not place_checker(board, column, CHECKERS[current_player]):
            print("Column full, turn lost.")
        else:
            clear_screen()
            print_board(board)

            if check_winner(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if is_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
