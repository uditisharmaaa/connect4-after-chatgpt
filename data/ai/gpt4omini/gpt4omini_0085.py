import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_empty_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, col, checker):
    row = get_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
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
    # Diagonal check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col_letter = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        
        if col_letter < 'A' or col_letter >= chr(65 + COLS):
            print("Invalid column letter! Please try again.")
            continue
        
        col = ord(col_letter) - 65
        if not place_checker(board, col, current_player):
            print("Column is full! Please try another column.")
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
