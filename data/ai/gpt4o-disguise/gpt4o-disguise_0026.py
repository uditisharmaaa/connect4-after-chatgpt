import random
import os

cols = 7
rows = 6
players = 2
checkers = ['X', 'O', 'V', 'H', 'M']  # limited to 5 players

def init_board():
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(ord('A') + c) for c in range(cols)]))
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")
    
def place_checker(board, col, checker):
    for r in range(rows-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False

def check_win(board):
    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != ' ':
                return True

    # Vertical check
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != ' ':
                return True

    # Diagonal check \
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != ' ':
                return True

    # Diagonal check /
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] != ' ':
                return True

    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = init_board()
    print_board(board)
    
    current_player = random.randint(0, players - 1)
    
    while True:
        print(f"Player {checkers[current_player]}, please enter a column:")
        while True:
            col_input = input().strip().upper()
            if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + cols - 1):
                col = ord(col_input) - ord('A')
                if place_checker(board, col, checkers[current_player]):
                    break
                else:
                    print("Column full. Try another column.")
            else:
                print("Invalid input, please enter a valid column.")
        
        print_board(board)
        
        if check_win(board):
            print(f"Player {checkers[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
