import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0]))) + "  "
    print(header)
    print("+" + ---+ * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + ---+ * len(board[0]))

def is_valid_move(board, col):
    return col < len(board[0]) and board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True
    # Vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True
    # Diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True
    # Diagonal (up-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        move = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        if len(move) != 1 or not 'A' <= move <= chr(64 + COLS) or not is_valid_move(board, ord(move) - 65):
            print("Invalid move. Try again.")
            continue
        
        place_checker(board, ord(move) -65, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
