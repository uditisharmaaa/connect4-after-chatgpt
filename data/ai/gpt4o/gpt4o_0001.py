import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"] # Player checkers symbols

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join([chr(i) for i in range(ord('A'), ord('A') + len(board[0]))])
    print(header)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(row) + "+")

def valid_input(input_str, col_count):
    return input_str.isalpha() and ord(input_str.upper()) - ord('A') < col_count

def get_column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def place_checker(board, column, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col+1] == checker and row[col+2] == checker and row[col+3] == checker:
                return True
    
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    
    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLS)
    print_board(board)
    
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_input = input("> ")

        if not valid_input(column_input, COLS):
            print("Invalid input. Enter a column letter.")
            continue
        
        column_index = get_column_index(column_input)
        
        if not place_checker(board, column_index, CHECKERS[current_player]):
            print("Column full. Turn lost.")
        else:
            print_board(board)

            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            
            if check_for_draw(board):
                print("The game is a draw!")
                break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
