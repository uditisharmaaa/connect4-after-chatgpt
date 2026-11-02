import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_column(col):
    return len(col) == 1 and col.isalpha() and ord(col.upper()) - 65 < COLS

def place_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None

def check_win(board, row, col):
    checker = board[row][col]
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1), # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row + step * dr, col + step * dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r += step * dr
                c += step * dc
                if count == 4:
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid column. Try again.")
            continue
        
        placed = place_checker(board, col, checker)
        if placed is None:
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        if check_win(board, placed[0], placed[1]):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
