import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    letters = [chr(65 + i) for i in range(COLUMNS)]
    print("  " + "   ".join(letters))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

def drop_checker(column, checker, board):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] != " " and board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] != " " and board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] != " " and board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] != " " and board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return True
    
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    
    clear_screen()
    print_board(board)
    
    while True:
        print(f"Player {players[current_player]}, please enter a column:")
        col_input = input().strip().upper()
        
        if len(col_input) != 1 or not col_input.isalpha() or ord(col_input) < 65 or ord(col_input) >= 65 + COLUMNS:
            print("Invalid input. Try again.")
            continue
        
        column = ord(col_input) - 65
        if not is_valid_column(column, board):
            print("Column is full or invalid. Try again.")
            continue
        
        drop_checker(column, players[current_player], board)
        clear_screen()
        print_board(board)
        
        if check_win(board):
            print(f"Player {players[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
