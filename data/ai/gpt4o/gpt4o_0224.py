import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support for up to 5 players

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = " ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_for_win(board, player):
    # Check horizontal, vertical, and diagonal wins.
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == player:
                # Horizontal
                if col <= len(board[0]) - 4 and all(board[row][col+i] == player for i in range(4)):
                    return True
                # Vertical
                if row <= len(board) - 4 and all(board[row+i][col] == player for i in range(4)):
                    return True
                # Diagonal /
                if row >= 3 and col <= len(board[0]) - 4 and all(board[row-i][col+i] == player for i in range(4)):
                    return True
                # Diagonal \
                if row <= len(board) - 4 and col <= len(board[0]) - 4 and all(board[row+i][col+i] == player for i in range(4)):
                    return True
    return False

def check_for_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def convert_input_to_index(input_str):
    return ord(input_str.upper()) - 65

def connect_4_game():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        while True:
            try:
                column_choice = input().strip()
                col_index = convert_input_to_index(column_choice)
                if is_valid_column(board, col_index):
                    break
                else:
                    print("Invalid input or column full. Please choose another column.")
            except:
                print("Invalid input or column full. Please choose another column.")
            
        place_checker(board, col_index, current_checker)
        print_board(board)
        
        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

connect_4_game()
