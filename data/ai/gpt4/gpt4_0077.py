import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    separator = "+---" * COLS + "+"
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == " "

def get_lowest_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, col, checker):
    row = get_lowest_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal check (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal check (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        draw_board(board)
        print(f"Player {players[current_player]}'s turn. Please enter a column:")
        
        col_input = input().strip()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue
        
        col = ord(col_input.upper()) - 65
        if not is_valid_column(board, col):
            print("Invalid column. Try again.")
            continue

        place_checker(board, col, players[current_player])
        if check_winner(board, players[current_player]):
            draw_board(board)
            print(f"Player {players[current_player]} won!")
            break
        if is_draw(board):
            draw_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
